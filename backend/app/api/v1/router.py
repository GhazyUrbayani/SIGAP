"""API v1 router — aggregates all route modules."""

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.kelurahan import router as kelurahan_router
from app.api.v1.uss import router as uss_router
from app.api.v1.alerts import router as alerts_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(kelurahan_router)
api_router.include_router(uss_router)
api_router.include_router(alerts_router)
