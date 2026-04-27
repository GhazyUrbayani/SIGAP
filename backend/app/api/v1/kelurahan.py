"""Kelurahan API routes — CRUD + spatial queries + GeoJSON."""

import json
from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from geoalchemy2.functions import ST_AsGeoJSON, ST_X, ST_Y
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.kelurahan import Kelurahan
from app.models.uss_score import USSScore
from app.models.user import User
from app.schemas.kelurahan import (
    KelurahanDetailResponse,
    KelurahanGeoJSONCollection,
    KelurahanGeoJSONFeature,
    KelurahanResponse,
)

router = APIRouter(prefix="/kelurahan", tags=["kelurahan"])


@router.get("", response_model=list[KelurahanResponse])
async def list_kelurahan(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    kota: Optional[str] = Query(None),
    kecamatan: Optional[str] = Query(None),
    level: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
):
    """List kelurahan with optional filters and latest USS."""
    # Subquery for latest USS per kelurahan
    latest_uss_sq = (
        select(
            USSScore.kelurahan_id,
            USSScore.uss,
            USSScore.uss_level,
            func.row_number()
            .over(
                partition_by=USSScore.kelurahan_id,
                order_by=USSScore.computed_at.desc(),
            )
            .label("rn"),
        )
        .subquery()
    )
    latest_uss = (
        select(latest_uss_sq)
        .where(latest_uss_sq.c.rn == 1)
        .subquery("latest_uss")
    )

    query = (
        select(Kelurahan, latest_uss.c.uss, latest_uss.c.uss_level)
        .outerjoin(latest_uss, Kelurahan.id == latest_uss.c.kelurahan_id)
    )

    if kota:
        query = query.where(Kelurahan.kota == kota)
    if kecamatan:
        query = query.where(Kelurahan.kecamatan == kecamatan)
    if level:
        query = query.where(latest_uss.c.uss_level == level)

    query = query.offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    rows = result.all()

    return [
        KelurahanResponse(
            id=str(kel.id),
            kode_bps=kel.kode_bps,
            nama=kel.nama,
            kecamatan=kel.kecamatan,
            kota=kel.kota,
            provinsi=kel.provinsi,
            luas_km2=float(kel.luas_km2) if kel.luas_km2 else None,
            populasi=kel.populasi,
            latest_uss=float(uss) if uss else None,
            uss_level=uss_level,
            created_at=kel.created_at,
        )
        for kel, uss, uss_level in rows
    ]


@router.get("/geojson")
async def get_geojson(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    kota: Optional[str] = Query(None),
):
    """Return GeoJSON FeatureCollection with USS data for map rendering."""
    # Subquery for latest USS
    latest_uss_sq = (
        select(
            USSScore.kelurahan_id,
            USSScore.uss,
            USSScore.uss_level,
            USSScore.climate_score,
            USSScore.infrastructure_score,
            USSScore.socioeconomic_score,
            USSScore.computed_at,
            func.row_number()
            .over(
                partition_by=USSScore.kelurahan_id,
                order_by=USSScore.computed_at.desc(),
            )
            .label("rn"),
        )
        .subquery()
    )
    latest_uss = (
        select(latest_uss_sq)
        .where(latest_uss_sq.c.rn == 1)
        .subquery("latest_uss")
    )

    query = select(
        Kelurahan.id,
        Kelurahan.nama,
        Kelurahan.kecamatan,
        Kelurahan.kota,
        Kelurahan.populasi,
        Kelurahan.luas_km2,
        ST_AsGeoJSON(Kelurahan.geometry).label("geojson"),
        latest_uss.c.uss,
        latest_uss.c.uss_level,
        latest_uss.c.climate_score,
        latest_uss.c.infrastructure_score,
        latest_uss.c.socioeconomic_score,
        latest_uss.c.computed_at,
    ).outerjoin(latest_uss, Kelurahan.id == latest_uss.c.kelurahan_id)

    if kota:
        query = query.where(Kelurahan.kota == kota)

    query = query.where(Kelurahan.geometry.isnot(None))

    result = await db.execute(query)
    rows = result.all()

    features = []
    for row in rows:
        if row.geojson:
            geom = json.loads(row.geojson)
            features.append({
                "type": "Feature",
                "properties": {
                    "id": str(row.id),
                    "nama": row.nama,
                    "kecamatan": row.kecamatan,
                    "kota": row.kota,
                    "populasi": row.populasi,
                    "luas_km2": float(row.luas_km2) if row.luas_km2 else None,
                    "uss": float(row.uss) if row.uss else None,
                    "uss_level": row.uss_level,
                    "climate_score": float(row.climate_score) if row.climate_score else None,
                    "infrastructure_score": float(row.infrastructure_score) if row.infrastructure_score else None,
                    "socioeconomic_score": float(row.socioeconomic_score) if row.socioeconomic_score else None,
                    "computed_at": row.computed_at.isoformat() if row.computed_at else None,
                },
                "geometry": geom,
            })

    return {"type": "FeatureCollection", "features": features}


@router.get("/{kelurahan_id}", response_model=KelurahanDetailResponse)
async def get_kelurahan(
    kelurahan_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Get detailed kelurahan data with latest USS breakdown."""
    result = await db.execute(select(Kelurahan).where(Kelurahan.id == kelurahan_id))
    kel = result.scalar_one_or_none()
    if not kel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kelurahan tidak ditemukan",
        )

    # Latest USS
    uss_result = await db.execute(
        select(USSScore)
        .where(USSScore.kelurahan_id == kelurahan_id)
        .order_by(USSScore.computed_at.desc())
        .limit(1)
    )
    latest = uss_result.scalar_one_or_none()

    return KelurahanDetailResponse(
        id=str(kel.id),
        kode_bps=kel.kode_bps,
        nama=kel.nama,
        kecamatan=kel.kecamatan,
        kota=kel.kota,
        provinsi=kel.provinsi,
        luas_km2=float(kel.luas_km2) if kel.luas_km2 else None,
        populasi=kel.populasi,
        latest_uss=float(latest.uss) if latest else None,
        uss_level=latest.uss_level if latest else None,
        climate_score=float(latest.climate_score) if latest else None,
        infrastructure_score=float(latest.infrastructure_score) if latest else None,
        socioeconomic_score=float(latest.socioeconomic_score) if latest else None,
        created_at=kel.created_at,
    )
