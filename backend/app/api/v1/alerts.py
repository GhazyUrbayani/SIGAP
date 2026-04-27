"""Alerts API routes."""

from datetime import datetime, timezone
from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.alert import Alert
from app.models.kelurahan import Kelurahan
from app.models.user import User
from app.schemas.alert import AlertListResponse, AlertResolveRequest, AlertResponse

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=AlertListResponse)
async def list_alerts(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    level: Optional[str] = Query(None),
    is_resolved: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    """List alerts with optional filters."""
    query = (
        select(Alert, Kelurahan.nama)
        .join(Kelurahan, Alert.kelurahan_id == Kelurahan.id)
    )

    if level:
        query = query.where(Alert.trigger_level == level)
    if is_resolved is not None:
        query = query.where(Alert.is_resolved == is_resolved)

    # Count
    count_q = select(func.count()).select_from(Alert)
    if level:
        count_q = count_q.where(Alert.trigger_level == level)
    if is_resolved is not None:
        count_q = count_q.where(Alert.is_resolved == is_resolved)
    total_result = await db.execute(count_q)
    total = total_result.scalar()

    query = query.order_by(Alert.created_at.desc()).offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    rows = result.all()

    return AlertListResponse(
        data=[
            AlertResponse(
                id=str(alert.id),
                kelurahan_id=str(alert.kelurahan_id),
                kelurahan_nama=nama,
                trigger_level=alert.trigger_level,
                uss_value=float(alert.uss_value),
                message=alert.message,
                is_resolved=alert.is_resolved,
                resolved_at=alert.resolved_at,
                created_at=alert.created_at,
            )
            for alert, nama in rows
        ],
        total=total,
    )


@router.patch("/{alert_id}/resolve", response_model=AlertResponse)
async def resolve_alert(
    alert_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Mark an alert as resolved."""
    result = await db.execute(select(Alert).where(Alert.id == alert_id))
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert tidak ditemukan")

    alert.is_resolved = True
    alert.resolved_at = datetime.now(timezone.utc)
    await db.flush()

    # Get kelurahan name
    kel_result = await db.execute(
        select(Kelurahan.nama).where(Kelurahan.id == alert.kelurahan_id)
    )
    nama = kel_result.scalar_one_or_none()

    return AlertResponse(
        id=str(alert.id),
        kelurahan_id=str(alert.kelurahan_id),
        kelurahan_nama=nama,
        trigger_level=alert.trigger_level,
        uss_value=float(alert.uss_value),
        message=alert.message,
        is_resolved=alert.is_resolved,
        resolved_at=alert.resolved_at,
        created_at=alert.created_at,
    )
