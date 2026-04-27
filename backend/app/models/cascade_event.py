"""Cascade Event ORM model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class CascadeEvent(Base):
    __tablename__ = "cascade_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    kelurahan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("kelurahan.id"), nullable=False
    )
    trigger_dimension: Mapped[str] = mapped_column(
        Enum("climate", "infrastructure", "socioeconomic", name="dimension_type",
             create_type=False),
        nullable=False,
    )
    affected_dimensions: Mapped[dict] = mapped_column(JSONB, nullable=False)
    correlation_score: Mapped[float] = mapped_column(Numeric(5, 4), nullable=False)
    event_description: Mapped[str] = mapped_column(Text, nullable=True)
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    kelurahan = relationship("Kelurahan", back_populates="cascade_events")
