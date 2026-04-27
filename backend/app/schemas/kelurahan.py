"""Kelurahan request/response schemas."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class KelurahanBase(BaseModel):
    kode_bps: str
    nama: str
    kecamatan: str
    kota: str
    provinsi: str


class KelurahanResponse(KelurahanBase):
    id: str
    luas_km2: Optional[float] = None
    populasi: Optional[int] = None
    latest_uss: Optional[float] = None
    uss_level: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class KelurahanDetailResponse(KelurahanResponse):
    climate_score: Optional[float] = None
    infrastructure_score: Optional[float] = None
    socioeconomic_score: Optional[float] = None


class KelurahanGeoJSONFeature(BaseModel):
    type: str = "Feature"
    properties: dict
    geometry: dict


class KelurahanGeoJSONCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List[KelurahanGeoJSONFeature]
