"""Kelurahan ORM model with PostGIS geometry."""

import uuid
from datetime import datetime

from geoalchemy2 import Geometry
from sqlalchemy import DateTime, Integer, Numeric, String, func, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Kelurahan(Base):
    __tablename__ = "kelurahan"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    kode_bps: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nama: Mapped[str] = mapped_column(String(255), nullable=False)
    kecamatan: Mapped[str] = mapped_column(String(255), nullable=False)
    kota: Mapped[str] = mapped_column(String(255), nullable=False)
    provinsi: Mapped[str] = mapped_column(String(255), nullable=False)
    geometry = mapped_column(Geometry("MULTIPOLYGON", srid=4326), nullable=True)
    centroid = mapped_column(Geometry("POINT", srid=4326), nullable=True)
    luas_km2: Mapped[float] = mapped_column(Numeric(10, 4), nullable=True)
    populasi: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    indicators = relationship("Indicator", back_populates="kelurahan", lazy="selectin")
    uss_scores = relationship("USSScore", back_populates="kelurahan", lazy="selectin")
    alerts = relationship("Alert", back_populates="kelurahan", lazy="selectin")
    cascade_events = relationship(
        "CascadeEvent", back_populates="kelurahan", lazy="selectin"
    )

    __table_args__ = (
        Index("idx_kelurahan_kota", "kota"),
    )
