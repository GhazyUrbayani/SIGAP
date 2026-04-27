"""Seed 5 kelurahan in Bandung with realistic geometry and demographics.

Uses realistic polygon geometries approximating actual Bandung kelurahan
boundaries. Centroids are computed from the polygons.
"""

import asyncio
import uuid
from datetime import datetime, timezone

from geoalchemy2 import WKTElement
from passlib.context import CryptContext
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_factory, engine
from app.models.kelurahan import Kelurahan
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 5 Kelurahan in Bandung with approximate polygon geometries
KELURAHAN_DATA = [
    {
        "kode_bps": "3273010001",
        "nama": "Coblong",
        "kecamatan": "Coblong",
        "kota": "Bandung",
        "provinsi": "Jawa Barat",
        "luas_km2": 7.35,
        "populasi": 45230,
        "polygon_wkt": "MULTIPOLYGON(((107.6100 -6.8800, 107.6200 -6.8800, 107.6200 -6.8900, 107.6150 -6.8950, 107.6100 -6.8900, 107.6100 -6.8800)))",
        "centroid_wkt": "POINT(107.6150 -6.8870)",
    },
    {
        "kode_bps": "3273010002",
        "nama": "Cicendo",
        "kecamatan": "Cicendo",
        "kota": "Bandung",
        "provinsi": "Jawa Barat",
        "luas_km2": 6.86,
        "populasi": 38750,
        "polygon_wkt": "MULTIPOLYGON(((107.5950 -6.9000, 107.6080 -6.9000, 107.6080 -6.9100, 107.6020 -6.9150, 107.5950 -6.9100, 107.5950 -6.9000)))",
        "centroid_wkt": "POINT(107.6015 -6.9050)",
    },
    {
        "kode_bps": "3273010003",
        "nama": "Sukasari",
        "kecamatan": "Sukasari",
        "kota": "Bandung",
        "provinsi": "Jawa Barat",
        "luas_km2": 6.27,
        "populasi": 52100,
        "polygon_wkt": "MULTIPOLYGON(((107.5900 -6.8650, 107.6050 -6.8650, 107.6050 -6.8780, 107.5980 -6.8820, 107.5900 -6.8780, 107.5900 -6.8650)))",
        "centroid_wkt": "POINT(107.5975 -6.8735)",
    },
    {
        "kode_bps": "3273010004",
        "nama": "Bandung Wetan",
        "kecamatan": "Bandung Wetan",
        "kota": "Bandung",
        "provinsi": "Jawa Barat",
        "luas_km2": 3.39,
        "populasi": 28900,
        "polygon_wkt": "MULTIPOLYGON(((107.6150 -6.9050, 107.6280 -6.9050, 107.6280 -6.9150, 107.6220 -6.9200, 107.6150 -6.9150, 107.6150 -6.9050)))",
        "centroid_wkt": "POINT(107.6215 -6.9120)",
    },
    {
        "kode_bps": "3273010005",
        "nama": "Cibeunying Kidul",
        "kecamatan": "Cibeunying Kidul",
        "kota": "Bandung",
        "provinsi": "Jawa Barat",
        "luas_km2": 5.03,
        "populasi": 41600,
        "polygon_wkt": "MULTIPOLYGON(((107.6250 -6.8850, 107.6380 -6.8850, 107.6380 -6.8970, 107.6320 -6.9010, 107.6250 -6.8970, 107.6250 -6.8850)))",
        "centroid_wkt": "POINT(107.6315 -6.8930)",
    },
]

SEED_USERS = [
    {
        "email": "admin@sigap.id",
        "password": "Admin123!",
        "full_name": "Admin SIGAP",
        "role": "admin",
    },
    {
        "email": "analyst@sigap.id",
        "password": "Analyst123!",
        "full_name": "Rini Analyst",
        "role": "analyst",
    },
    {
        "email": "viewer@sigap.id",
        "password": "Viewer123!",
        "full_name": "Dani Viewer",
        "role": "viewer",
    },
]


async def seed():
    async with async_session_factory() as db:
        # Seed users
        for u in SEED_USERS:
            user = User(
                email=u["email"],
                hashed_password=pwd_context.hash(u["password"]),
                full_name=u["full_name"],
                role=u["role"],
            )
            db.add(user)

        # Seed kelurahan
        for k in KELURAHAN_DATA:
            kel = Kelurahan(
                kode_bps=k["kode_bps"],
                nama=k["nama"],
                kecamatan=k["kecamatan"],
                kota=k["kota"],
                provinsi=k["provinsi"],
                luas_km2=k["luas_km2"],
                populasi=k["populasi"],
                geometry=WKTElement(k["polygon_wkt"], srid=4326),
                centroid=WKTElement(k["centroid_wkt"], srid=4326),
            )
            db.add(kel)

        await db.commit()
        print("✅ Seeded 5 kelurahan + 3 users for Bandung")


if __name__ == "__main__":
    asyncio.run(seed())
