"""USS Score ORM model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class USSScore(Base):
    __tablename__ = "uss_scores"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    kelurahan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("kelurahan.id"), nullable=False
    )
    uss: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    climate_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    infrastructure_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    socioeconomic_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    uss_level: Mapped[str] = mapped_column(
        Enum("very_low", "low", "medium", "high", "very_high", name="uss_level_type"),
        nullable=False,
    )
    model_version: Mapped[str] = mapped_column(String(50), nullable=True)
    computed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    kelurahan = relationship("Kelurahan", back_populates="uss_scores")
    alerts = relationship("Alert", back_populates="uss_score", lazy="selectin")

    __table_args__ = (
        Index("idx_uss_kelurahan_computed_at", "kelurahan_id", "computed_at"),
        Index("idx_uss_level", "uss_level"),
    )
