"""FastAPI application entry point.

Creates the app with:
- CORS middleware for frontend dev server
- Health check endpoint
- API v1 router aggregate
- APScheduler startup for periodic jobs
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.config import get_settings
from app.tasks.scheduler import start_scheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    logger.info("🚀 SIGAP Backend starting up...")
    start_scheduler()
    yield
    logger.info("👋 SIGAP Backend shutting down...")


app = FastAPI(
    title="SIGAP API",
    description="Sistem Intelijen Geospasial Ancaman Perkotaan — Backend API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Ensure CORS headers are appended even for unhandled 500 errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    origin = request.headers.get("origin")
    headers = {}
    if origin in settings.cors_origins_list or "*" in settings.cors_origins_list:
        headers["Access-Control-Allow-Origin"] = origin
        headers["Access-Control-Allow-Credentials"] = "true"
    
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
        headers=headers,
    )

# Routes
app.include_router(api_router)


@app.get("/health")
async def health_check():
    """Health check endpoint for load balancers and monitoring."""
    return {"status": "healthy", "service": "sigap-backend", "version": "1.0.0"}
