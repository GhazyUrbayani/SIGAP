"""Seed dummy indicator data for all kelurahan.

Generates realistic indicator values based on Bandung climate/infra patterns.
Creates 30 days of historical data for trend charts.
"""

import asyncio
import random
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_factory
from app.models.indicator import Indicator
from app.models.kelurahan import Kelurahan

# Realistic indicator profiles per kelurahan (stress level: low/med/high)
PROFILES = {
    "Coblong": "medium",
    "Cicendo": "high",
    "Sukasari": "very_high",
    "Bandung Wetan": "low",
    "Cibeunying Kidul": "high",
}

INDICATOR_CONFIGS = {
    "low": {
        "climate": {
            "rainfall_intensity": (20, 60),
            "flood_frequency": (0, 2),
            "temperature_anomaly": (0, 1),
            "humidity_index": (65, 75),
        },
        "infrastructure": {
            "road_damage_ratio": (0.05, 0.15),
            "drainage_quality": (0.7, 0.9),
            "building_density": (50, 150),
            "green_space_ratio": (0.2, 0.35),
        },
        "socioeconomic": {
            "poverty_rate": (3, 8),
            "unemployment_rate": (2, 5),
            "health_facility_access": (0.7, 0.9),
            "education_index": (0.7, 0.85),
        },
    },
    "medium": {
        "climate": {
            "rainfall_intensity": (60, 120),
            "flood_frequency": (2, 5),
            "temperature_anomaly": (1, 2.5),
            "humidity_index": (75, 85),
        },
        "infrastructure": {
            "road_damage_ratio": (0.2, 0.4),
            "drainage_quality": (0.4, 0.65),
            "building_density": (150, 300),
            "green_space_ratio": (0.1, 0.2),
        },
        "socioeconomic": {
            "poverty_rate": (10, 18),
            "unemployment_rate": (5, 10),
            "health_facility_access": (0.4, 0.65),
            "education_index": (0.5, 0.65),
        },
    },
    "high": {
        "climate": {
            "rainfall_intensity": (120, 200),
            "flood_frequency": (5, 9),
            "temperature_anomaly": (2, 3.5),
            "humidity_index": (82, 92),
        },
        "infrastructure": {
            "road_damage_ratio": (0.4, 0.65),
            "drainage_quality": (0.25, 0.45),
            "building_density": (250, 400),
            "green_space_ratio": (0.05, 0.12),
        },
        "socioeconomic": {
            "poverty_rate": (18, 28),
            "unemployment_rate": (9, 14),
            "health_facility_access": (0.25, 0.45),
            "education_index": (0.35, 0.5),
        },
    },
    "very_high": {
        "climate": {
            "rainfall_intensity": (180, 280),
            "flood_frequency": (8, 12),
            "temperature_anomaly": (3, 4.5),
            "humidity_index": (88, 98),
        },
        "infrastructure": {
            "road_damage_ratio": (0.6, 0.85),
            "drainage_quality": (0.1, 0.3),
            "building_density": (350, 480),
            "green_space_ratio": (0.02, 0.08),
        },
        "socioeconomic": {
            "poverty_rate": (25, 38),
            "unemployment_rate": (12, 18),
            "health_facility_access": (0.1, 0.3),
            "education_index": (0.2, 0.4),
        },
    },
}

UNITS = {
    "rainfall_intensity": "mm/jam",
    "flood_frequency": "kejadian/tahun",
    "temperature_anomaly": "°C",
    "humidity_index": "%",
    "road_damage_ratio": "rasio",
    "drainage_quality": "rasio",
    "building_density": "bangunan/km²",
    "green_space_ratio": "rasio",
    "poverty_rate": "%",
    "unemployment_rate": "%",
    "health_facility_access": "rasio",
    "education_index": "indeks",
}

SOURCES = {
    "climate": "BMKG",
    "infrastructure": "OSM/PUPR",
    "socioeconomic": "BPS",
}


async def seed():
    async with async_session_factory() as db:
        result = await db.execute(select(Kelurahan))
        kelurahan_list = result.scalars().all()

        now = datetime.now(timezone.utc)
        count = 0

        for kel in kelurahan_list:
            profile = PROFILES.get(kel.nama, "medium")
            config = INDICATOR_CONFIGS[profile]

            # Generate 30 days of data
            for day_offset in range(30):
                recorded_at = now - timedelta(days=29 - day_offset)

                for dimension, indicators in config.items():
                    for key, (lo, hi) in indicators.items():
                        # Add some day-to-day variance
                        val = random.uniform(lo, hi)
                        # Add slight trend (things getting slightly worse)
                        val += day_offset * 0.01 * val * random.uniform(-0.5, 1.0)
                        val = max(lo * 0.8, min(hi * 1.2, val))

                        indicator = Indicator(
                            kelurahan_id=kel.id,
                            dimension=dimension,
                            indicator_key=key,
                            value=round(val, 6),
                            unit=UNITS[key],
                            source=SOURCES[dimension],
                            recorded_at=recorded_at,
                        )
                        db.add(indicator)
                        count += 1

        await db.commit()
        print(f"✅ Seeded {count} indicator records (30 days × 5 kelurahan × 12 indicators)")


if __name__ == "__main__":
    asyncio.run(seed())
