"""USS request/response schemas."""

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel


class USSLatestItem(BaseModel):
    kelurahan_id: str
    nama: str
    uss: float
    uss_level: str
    climate_score: float
    infrastructure_score: float
    socioeconomic_score: float
    computed_at: datetime


class USSLatestResponse(BaseModel):
    data: List[USSLatestItem]
    total: int
    computed_at: Optional[datetime] = None


class USSHistoryItem(BaseModel):
    uss: float
    climate_score: float
    infrastructure_score: float
    socioeconomic_score: float
    uss_level: str
    computed_at: datetime


class USSHistoryResponse(BaseModel):
    kelurahan_id: str
    nama: str
    history: List[USSHistoryItem]


class SimulateRequest(BaseModel):
    kelurahan_id: str
    overrides: Dict[str, Dict[str, float]]


class SimulateResponse(BaseModel):
    original_uss: float
    simulated_uss: float
    delta: float
    breakdown: Dict[str, float]


class ScenarioRequest(BaseModel):
    kelurahan_id: str
    drainase_improvement: float = 0.0
    road_repair: float = 0.0
    social_program: float = 0.0
    projection_months: int = 12


class ProjectionPoint(BaseModel):
    month: int
    uss: float


class ScenarioResponse(BaseModel):
    kelurahan_id: str
    nama: str
    current_uss: float
    baseline_projection: List[ProjectionPoint]
    intervention_projection: List[ProjectionPoint]
    estimated_reduction: float
