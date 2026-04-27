"""Run initial USS computation for all seeded kelurahan.

Reads latest indicators from DB, computes USS using the engine,
stores results in uss_scores table, and triggers alert generation.
Creates 30 days of historical USS scores for trend charts.
"""

import asyncio
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_factory
from app.models.indicator import Indicator
from app.models.kelurahan import Kelurahan
from app.models.uss_score import USSScore
from app.services.alert_engine import check_and_create_alerts
from app.services.uss_engine import USSEngine


async def run():
    engine = USSEngine()

    async with async_session_factory() as db:
        result = await db.execute(select(Kelurahan))
        kelurahan_list = result.scalars().all()
        now = datetime.now(timezone.utc)

        for kel in kelurahan_list:
            # Get all indicators for this kelurahan
            ind_result = await db.execute(
                select(Indicator)
                .where(Indicator.kelurahan_id == kel.id)
                .order_by(Indicator.recorded_at.asc())
            )
            all_indicators = ind_result.scalars().all()

            # Group by day
            days = {}
            for ind in all_indicators:
                day = ind.recorded_at.date()
                if day not in days:
                    days[day] = {}
                days[day][ind.indicator_key] = float(ind.value)

            # Compute USS for each day (historical scores)
            for day_date, ind_dict in sorted(days.items()):
                uss_result = engine.compute_uss(ind_dict)
                computed_at = datetime.combine(
                    day_date, datetime.min.time(), tzinfo=timezone.utc
                )

                score = USSScore(
                    kelurahan_id=kel.id,
                    uss=uss_result["uss"],
                    climate_score=uss_result["climate_score"],
                    infrastructure_score=uss_result["infrastructure_score"],
                    socioeconomic_score=uss_result["socioeconomic_score"],
                    uss_level=uss_result["uss_level"],
                    model_version="v1.0.0-prototype",
                    computed_at=computed_at,
                )
                db.add(score)

            print(f"  ✅ {kel.nama}: {len(days)} USS scores computed")

        # Create alerts for latest scores
        alerts = await check_and_create_alerts(db)
        print(f"  🔔 {len(alerts)} alerts created")

        await db.commit()
        print("✅ Initial USS computation complete")


if __name__ == "__main__":
    asyncio.run(run())
