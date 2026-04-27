"""Initial migration — all tables with PostGIS.

Revision ID: 001_initial
Revises: None
Create Date: 2026-04-27
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import geoalchemy2
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enable PostGIS extension
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    # Users table
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("role", sa.Enum("admin", "analyst", "viewer", name="user_role"), nullable=False),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Kelurahan table
    op.create_table(
        "kelurahan",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("kode_bps", sa.String(20), unique=True, nullable=False),
        sa.Column("nama", sa.String(255), nullable=False),
        sa.Column("kecamatan", sa.String(255), nullable=False),
        sa.Column("kota", sa.String(255), nullable=False),
        sa.Column("provinsi", sa.String(255), nullable=False),
        sa.Column("geometry", geoalchemy2.Geometry("MULTIPOLYGON", srid=4326), nullable=True),
        sa.Column("centroid", geoalchemy2.Geometry("POINT", srid=4326), nullable=True),
        sa.Column("luas_km2", sa.Numeric(10, 4), nullable=True),
        sa.Column("populasi", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("idx_kelurahan_kota", "kelurahan", ["kota"])

    # Indicators table
    op.create_table(
        "indicators",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("kelurahan_id", UUID(as_uuid=True), sa.ForeignKey("kelurahan.id"), nullable=False),
        sa.Column("dimension", sa.Enum("climate", "infrastructure", "socioeconomic", name="dimension_type"), nullable=False),
        sa.Column("indicator_key", sa.String(100), nullable=False),
        sa.Column("value", sa.Numeric(15, 6), nullable=False),
        sa.Column("unit", sa.String(50), nullable=True),
        sa.Column("source", sa.String(100), nullable=True),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ingested_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("idx_indicators_kelurahan_dimension", "indicators", ["kelurahan_id", "dimension"])
    op.create_index("idx_indicators_recorded_at", "indicators", ["recorded_at"])

    # USS Scores table
    op.create_table(
        "uss_scores",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("kelurahan_id", UUID(as_uuid=True), sa.ForeignKey("kelurahan.id"), nullable=False),
        sa.Column("uss", sa.Numeric(5, 2), nullable=False),
        sa.Column("climate_score", sa.Numeric(5, 2), nullable=False),
        sa.Column("infrastructure_score", sa.Numeric(5, 2), nullable=False),
        sa.Column("socioeconomic_score", sa.Numeric(5, 2), nullable=False),
        sa.Column("uss_level", sa.Enum("very_low", "low", "medium", "high", "very_high", name="uss_level_type"), nullable=False),
        sa.Column("model_version", sa.String(50), nullable=True),
        sa.Column("computed_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("idx_uss_kelurahan_computed_at", "uss_scores", ["kelurahan_id", "computed_at"])
    op.create_index("idx_uss_level", "uss_scores", ["uss_level"])

    # Alerts table
    op.create_table(
        "alerts",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("kelurahan_id", UUID(as_uuid=True), sa.ForeignKey("kelurahan.id"), nullable=False),
        sa.Column("uss_score_id", UUID(as_uuid=True), sa.ForeignKey("uss_scores.id"), nullable=False),
        sa.Column("trigger_level", sa.Enum("watch", "warning", "emergency", name="trigger_level_type"), nullable=False),
        sa.Column("uss_value", sa.Numeric(5, 2), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("is_resolved", sa.Boolean(), default=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Cascade Events table
    op.create_table(
        "cascade_events",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("kelurahan_id", UUID(as_uuid=True), sa.ForeignKey("kelurahan.id"), nullable=False),
        sa.Column("trigger_dimension", sa.Enum("climate", "infrastructure", "socioeconomic", name="dimension_type", create_type=False), nullable=False),
        sa.Column("affected_dimensions", JSONB(), nullable=False),
        sa.Column("correlation_score", sa.Numeric(5, 4), nullable=False),
        sa.Column("event_description", sa.Text(), nullable=True),
        sa.Column("detected_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("cascade_events")
    op.drop_table("alerts")
    op.drop_table("uss_scores")
    op.drop_table("indicators")
    op.drop_table("kelurahan")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS trigger_level_type")
    op.execute("DROP TYPE IF EXISTS uss_level_type")
    op.execute("DROP TYPE IF EXISTS dimension_type")
    op.execute("DROP TYPE IF EXISTS user_role")
