"""USS API routes — latest scores, history, and simulation."""

import json
from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.kelurahan import Kelurahan
from app.models.uss_score import USSScore
from app.models.user import User
from app.schemas.uss import (
    ScenarioRequest,
    ScenarioResponse,
    SimulateRequest,
    SimulateResponse,
    USSHistoryItem,
    USSHistoryResponse,
    USSLatestItem,
    USSLatestResponse,
    ProjectionPoint,
)
from app.services.uss_engine import USSEngine

router = APIRouter(prefix="/uss", tags=["uss"])


@router.get("/latest", response_model=USSLatestResponse)
async def get_latest_uss(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    kota: str = Query("Bandung"),
):
    """Get latest USS for all kelurahan in a city.

    Uses Redis cache if available, falls back to DB.
    """
    from sqlalchemy import func

    # Subquery: latest USS per kelurahan
    latest_sq = (
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
    latest = select(latest_sq).where(latest_sq.c.rn == 1).subquery("latest")

    query = (
        select(
            Kelurahan.id,
            Kelurahan.nama,
            latest.c.uss,
            latest.c.uss_level,
            latest.c.climate_score,
            latest.c.infrastructure_score,
            latest.c.socioeconomic_score,
            latest.c.computed_at,
        )
        .join(latest, Kelurahan.id == latest.c.kelurahan_id)
        .where(Kelurahan.kota == kota)
        .order_by(latest.c.uss.desc())
    )

    result = await db.execute(query)
    rows = result.all()

    items = [
        USSLatestItem(
            kelurahan_id=str(row.id),
            nama=row.nama,
            uss=float(row.uss),
            uss_level=row.uss_level,
            climate_score=float(row.climate_score),
            infrastructure_score=float(row.infrastructure_score),
            socioeconomic_score=float(row.socioeconomic_score),
            computed_at=row.computed_at,
        )
        for row in rows
    ]

    latest_computed = max((i.computed_at for i in items), default=None) if items else None

    return USSLatestResponse(
        data=items,
        total=len(items),
        computed_at=latest_computed,
    )


@router.get("/{kelurahan_id}/history", response_model=USSHistoryResponse)
async def get_uss_history(
    kelurahan_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    limit: int = Query(30, ge=1, le=365),
):
    """Get USS history for a specific kelurahan."""
    # Verify kelurahan exists
    kel_result = await db.execute(
        select(Kelurahan).where(Kelurahan.id == kelurahan_id)
    )
    kel = kel_result.scalar_one_or_none()
    if not kel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kelurahan tidak ditemukan",
        )

    result = await db.execute(
        select(USSScore)
        .where(USSScore.kelurahan_id == kelurahan_id)
        .order_by(USSScore.computed_at.desc())
        .limit(limit)
    )
    scores = result.scalars().all()

    return USSHistoryResponse(
        kelurahan_id=str(kelurahan_id),
        nama=kel.nama,
        history=[
            USSHistoryItem(
                uss=float(s.uss),
                climate_score=float(s.climate_score),
                infrastructure_score=float(s.infrastructure_score),
                socioeconomic_score=float(s.socioeconomic_score),
                uss_level=s.uss_level,
                computed_at=s.computed_at,
            )
            for s in reversed(scores)
        ],
    )


@router.post("/simulate", response_model=SimulateResponse)
async def simulate_uss(
    body: SimulateRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Simulate USS with modified indicator values."""
    kelurahan_id = UUID(body.kelurahan_id)

    # Get current USS
    result = await db.execute(
        select(USSScore)
        .where(USSScore.kelurahan_id == kelurahan_id)
        .order_by(USSScore.computed_at.desc())
        .limit(1)
    )
    current = result.scalar_one_or_none()
    if not current:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="USS belum dihitung untuk kelurahan ini",
        )

    engine = USSEngine()
    simulated = engine.simulate(
        current_climate=float(current.climate_score),
        current_infra=float(current.infrastructure_score),
        current_soceco=float(current.socioeconomic_score),
        overrides=body.overrides,
    )

    return SimulateResponse(
        original_uss=float(current.uss),
        simulated_uss=simulated["uss"],
        delta=round(simulated["uss"] - float(current.uss), 2),
        breakdown=simulated["breakdown"],
    )


@router.post("/scenario", response_model=ScenarioResponse)
async def run_scenario(
    body: ScenarioRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Run scenario projection with infrastructure delta parameters.

    Projects USS for 12, 24, 36, or 60 months comparing baseline vs intervention.
    """
    kelurahan_id = UUID(body.kelurahan_id)

    kel_result = await db.execute(
        select(Kelurahan).where(Kelurahan.id == kelurahan_id)
    )
    kel = kel_result.scalar_one_or_none()
    if not kel:
        raise HTTPException(status_code=404, detail="Kelurahan tidak ditemukan")

    result = await db.execute(
        select(USSScore)
        .where(USSScore.kelurahan_id == kelurahan_id)
        .order_by(USSScore.computed_at.desc())
        .limit(1)
    )
    current = result.scalar_one_or_none()
    if not current:
        raise HTTPException(status_code=404, detail="USS belum dihitung")

    engine = USSEngine()
    projection = engine.project_scenario(
        current_uss=float(current.uss),
        current_climate=float(current.climate_score),
        current_infra=float(current.infrastructure_score),
        current_soceco=float(current.socioeconomic_score),
        drainase_improvement=body.drainase_improvement,
        road_repair=body.road_repair,
        social_program=body.social_program,
        months=body.projection_months,
    )

    return ScenarioResponse(
        kelurahan_id=str(kelurahan_id),
        nama=kel.nama,
        current_uss=float(current.uss),
        baseline_projection=projection["baseline"],
        intervention_projection=projection["intervention"],
        estimated_reduction=projection["estimated_reduction"],
    )
