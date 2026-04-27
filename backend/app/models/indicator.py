"""Indicator ORM model — stores raw data from external sources."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Indicator(Base):
    __tablename__ = "indicators"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    kelurahan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("kelurahan.id"), nullable=False
    )
    dimension: Mapped[str] = mapped_column(
        Enum("climate", "infrastructure", "socioeconomic", name="dimension_type"),
        nullable=False,
    )
    indicator_key: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[float] = mapped_column(Numeric(15, 6), nullable=False)
    unit: Mapped[str] = mapped_column(String(50), nullable=True)
    source: Mapped[str] = mapped_column(String(100), nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    kelurahan = relationship("Kelurahan", back_populates="indicators")

    __table_args__ = (
        Index("idx_indicators_kelurahan_dimension", "kelurahan_id", "dimension"),
        Index("idx_indicators_recorded_at", "recorded_at"),
    )
