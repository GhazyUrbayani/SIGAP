"""Alert Engine — threshold-based alert generation with NLG templates.

Generates actionable alerts in Bahasa Indonesia when USS thresholds
are breached. Uses rule-based NLG with data-driven templates.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.alert import Alert
from app.models.kelurahan import Kelurahan
from app.models.uss_score import USSScore


# Alert thresholds per PRD spec
TRIGGER_THRESHOLDS = {
    "watch": (60, 69),
    "warning": (70, 79),
    "emergency": (80, 100),
}

# NLG templates in Bahasa Indonesia — rule-based, specific, actionable
ALERT_TEMPLATES = {
    "watch": (
        "⚠️ WASPADA — Kelurahan {nama} mencatat USS {uss}/100 (level Watch). "
        "Dimensi tertinggi: {top_dim} ({top_score}/100). "
        "Rekomendasi: Monitor kondisi {top_dim_label} secara berkala dan "
        "siapkan rencana kontingensi dalam 7 hari ke depan."
    ),
    "warning": (
        "🔶 PERINGATAN — Kelurahan {nama} dalam zona KUNING dengan USS {uss}/100. "
        "Tekanan tertinggi berasal dari dimensi {top_dim_label} ({top_score}/100). "
        "Indikator kritis mencapai {anomaly_pct}% di atas baseline normal. "
        "Rekomendasi: Lakukan inspeksi lapangan di area terdampak dan "
        "koordinasikan dengan BPBD dalam 48 jam."
    ),
    "emergency": (
        "🔴 DARURAT — Kelurahan {nama} memasuki zona MERAH dengan USS {uss}/100. "
        "Risiko cascading failure terdeteksi: {top_dim_label} ({top_score}/100) "
        "berpotensi memicu degradasi lintas dimensi. "
        "Tindakan segera: 1) Aktifkan posko tanggap darurat, "
        "2) Kerahkan tim inspeksi ke RW prioritas, "
        "3) Siapkan laporan eskalasi ke Kepala Daerah. Batas waktu: 24 jam."
    ),
}

DIMENSION_LABELS = {
    "climate": "Iklim",
    "infrastructure": "Infrastruktur",
    "socioeconomic": "Sosial-Ekonomi",
}


def determine_trigger_level(uss: float) -> Optional[str]:
    """Determine alert trigger level based on USS value.

    Args:
        uss: USS score 0-100.

    Returns:
        Trigger level string or None if below watch threshold.
    """
    if uss >= 80:
        return "emergency"
    elif uss >= 70:
        return "warning"
    elif uss >= 60:
        return "watch"
    return None


def generate_alert_message(
    nama: str,
    uss: float,
    climate: float,
    infra: float,
    soceco: float,
    level: str,
) -> str:
    """Generate NLG alert message from template with real data.

    Args:
        nama: Kelurahan name.
        uss: USS score.
        climate: Climate dimension score.
        infra: Infrastructure dimension score.
        soceco: Socioeconomic dimension score.
        level: Trigger level.

    Returns:
        Formatted alert message in Bahasa Indonesia.
    """
    scores = {
        "climate": climate,
        "infrastructure": infra,
        "socioeconomic": soceco,
    }
    top_dim = max(scores, key=scores.get)
    top_score = scores[top_dim]

    # Anomaly percentage approximation (deviation from healthy baseline of 40)
    anomaly_pct = round(max(0, (top_score - 40) / 40 * 100), 0)

    template = ALERT_TEMPLATES.get(level, ALERT_TEMPLATES["watch"])
    return template.format(
        nama=nama,
        uss=uss,
        top_dim=top_dim,
        top_dim_label=DIMENSION_LABELS.get(top_dim, top_dim),
        top_score=top_score,
        anomaly_pct=int(anomaly_pct),
    )


async def check_and_create_alerts(db: AsyncSession) -> List[Alert]:
    """Check all latest USS scores and create alerts for threshold breaches.

    Args:
        db: Async database session.

    Returns:
        List of newly created Alert records.
    """
    from sqlalchemy import func

    # Get latest USS per kelurahan
    latest_sq = (
        select(
            USSScore.id.label("uss_id"),
            USSScore.kelurahan_id,
            USSScore.uss,
            USSScore.climate_score,
            USSScore.infrastructure_score,
            USSScore.socioeconomic_score,
            func.row_number()
            .over(
                partition_by=USSScore.kelurahan_id,
                order_by=USSScore.computed_at.desc(),
            )
            .label("rn"),
        )
        .subquery()
    )
    latest = select(latest_sq).where(latest_sq.c.rn == 1).subquery()

    query = select(
        Kelurahan.id,
        Kelurahan.nama,
        latest.c.uss_id,
        latest.c.uss,
        latest.c.climate_score,
        latest.c.infrastructure_score,
        latest.c.socioeconomic_score,
    ).join(latest, Kelurahan.id == latest.c.kelurahan_id)

    result = await db.execute(query)
    rows = result.all()

    new_alerts = []
    for row in rows:
        level = determine_trigger_level(float(row.uss))
        if not level:
            continue

        # Check if active (unresolved) alert already exists for this kelurahan
        existing = await db.execute(
            select(Alert)
            .where(Alert.kelurahan_id == row.id)
            .where(Alert.is_resolved == False)
            .where(Alert.trigger_level == level)
        )
        if existing.scalar_one_or_none():
            continue

        message = generate_alert_message(
            nama=row.nama,
            uss=float(row.uss),
            climate=float(row.climate_score),
            infra=float(row.infrastructure_score),
            soceco=float(row.socioeconomic_score),
            level=level,
        )

        alert = Alert(
            kelurahan_id=row.id,
            uss_score_id=row.uss_id,
            trigger_level=level,
            uss_value=float(row.uss),
            message=message,
        )
        db.add(alert)
        new_alerts.append(alert)

    if new_alerts:
        await db.flush()

    return new_alerts
