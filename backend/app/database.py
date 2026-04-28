"""Database session factory with async SQLAlchemy + PostGIS support."""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

import ssl
from urllib.parse import parse_qsl, urlencode, urlparse
from app.config import get_settings

settings = get_settings()


def normalize_async_url(url: str) -> str:
    """Return an async DB URL without unsupported query params."""
    parsed = urlparse(url)
    if not parsed.query:
        return url

    query_pairs = [
        (key, value)
        for key, value in parse_qsl(parsed.query, keep_blank_values=True)
        if key.lower() != "sslmode"
    ]
    return parsed._replace(query=urlencode(query_pairs)).geturl()

connect_args = {}
if settings.REQUIRE_SSL:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    connect_args["ssl"] = ctx

engine = create_async_engine(
    normalize_async_url(settings.DATABASE_URL),
    echo=settings.APP_DEBUG,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    connect_args=connect_args,
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


async def get_db() -> AsyncSession:
    """Dependency: yield an async database session."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
