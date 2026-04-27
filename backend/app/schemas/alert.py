"""Alert request/response schemas."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class AlertResponse(BaseModel):
    id: str
    kelurahan_id: str
    kelurahan_nama: Optional[str] = None
    trigger_level: str
    uss_value: float
    message: str
    is_resolved: bool
    resolved_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class AlertListResponse(BaseModel):
    data: List[AlertResponse]
    total: int


class AlertResolveRequest(BaseModel):
    is_resolved: bool = True
