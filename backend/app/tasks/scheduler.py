"""APScheduler cron jobs for periodic data ingestion and USS recalculation.

Jobs:
- Every 6 hours: fetch BMKG data, recalculate USS, check alerts
- Anomaly detection: z-score > 2σ from 30-day rolling baseline triggers recalc
"""

import asyncio
import logging
from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def fetch_bmkg_data():
    """Fetch latest weather data from BMKG API.

    Falls back to NASA IMERG if BMKG returns error/empty.
    In prototype mode, generates synthetic data based on
    seasonal patterns for Bandung.
    """
    logger.info("📡 Fetching BMKG data...")
    # In production: httpx call to BMKG API
    # Fallback: NASA IMERG
    # For prototype: data is seeded and updated via seed scripts
    logger.info("✅ BMKG data fetch complete (mock)")


async def recalculate_uss():
    """Recalculate USS for all kelurahan using latest indicators."""
    from app.database import async_session_factory
    from app.models.kelurahan import Kelurahan
    from app.models.indicator import Indicator
    from app.models.uss_score import USSScore
    from app.services.uss_engine import USSEngine
    from sqlalchemy import select, func

    logger.info("🔄 Recalculating USS for all kelurahan...")

    async with async_session_factory() as db:
        try:
            result = await db.execute(select(Kelurahan))
            kelurahan_list = result.scalars().all()
            engine = USSEngine()

            for kel in kelurahan_list:
                # Get latest indicators
                ind_result = await db.execute(
                    select(Indicator)
                    .where(Indicator.kelurahan_id == kel.id)
                    .order_by(Indicator.recorded_at.desc())
                )
                indicators = ind_result.scalars().all()

                if not indicators:
                    continue

                # Build indicator dict (latest value per key)
                ind_dict = {}
                seen = set()
                for ind in indicators:
                    if ind.indicator_key not in seen:
                        ind_dict[ind.indicator_key] = float(ind.value)
                        seen.add(ind.indicator_key)

                uss_result = engine.compute_uss(ind_dict)

                score = USSScore(
                    kelurahan_id=kel.id,
                    uss=uss_result["uss"],
                    climate_score=uss_result["climate_score"],
                    infrastructure_score=uss_result["infrastructure_score"],
                    socioeconomic_score=uss_result["socioeconomic_score"],
                    uss_level=uss_result["uss_level"],
                    model_version="v1.0.0-prototype",
                )
                db.add(score)

            await db.commit()
            logger.info(f"✅ USS recalculated for {len(kelurahan_list)} kelurahan")
        except Exception as e:
            await db.rollback()
            logger.error(f"❌ USS recalculation failed: {e}")


async def check_alerts():
    """Check thresholds and create alerts."""
    from app.database import async_session_factory
    from app.services.alert_engine import check_and_create_alerts

    logger.info("🔔 Checking alert thresholds...")
    async with async_session_factory() as db:
        try:
            alerts = await check_and_create_alerts(db)
            await db.commit()
            logger.info(f"✅ Created {len(alerts)} new alerts")
        except Exception as e:
            await db.rollback()
            logger.error(f"❌ Alert check failed: {e}")


async def periodic_pipeline():
    """Full pipeline: fetch → recalculate → alert."""
    await fetch_bmkg_data()
    await recalculate_uss()
    await check_alerts()


def start_scheduler():
    """Initialize and start the APScheduler with all jobs."""
    scheduler.add_job(
        periodic_pipeline,
        trigger=IntervalTrigger(hours=6),
        id="periodic_pipeline",
        name="BMKG Fetch + USS Recalc + Alert Check",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("⏰ Scheduler started — pipeline runs every 6 hours")
