"""SIGAP application configuration via pydantic-settings."""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App
    APP_ENV: str = "development"
    APP_DEBUG: bool = True

    # Database — Render/Azure provide a full DATABASE_URL directly.
    # For local dev, we compose it from individual POSTGRES_* vars.
    DATABASE_URL_RAW: str = ""  # Direct URL from cloud provider
    POSTGRES_USER: str = "sigap"
    POSTGRES_PASSWORD: str = "sigap_dev_password"
    POSTGRES_DB: str = "sigap_db"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    @property
    def DATABASE_URL(self) -> str:
        if self.DATABASE_URL_RAW:
            url = self.DATABASE_URL_RAW
            # Render gives postgres:// but asyncpg needs postgresql+asyncpg://
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
            if "postgresql://" in url and "+asyncpg" not in url:
                url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
            
            # Remove sslmode=require for asyncpg
            if "?sslmode=require" in url:
                url = url.replace("?sslmode=require", "")
            elif "&sslmode=require" in url:
                url = url.replace("&sslmode=require", "")
            
            return url
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def REQUIRE_SSL(self) -> bool:
        if self.DATABASE_URL_RAW and "sslmode=require" in self.DATABASE_URL_RAW.lower():
            return True
        return False

    @property
    def DATABASE_URL_SYNC(self) -> str:
        if self.DATABASE_URL_RAW:
            url = self.DATABASE_URL_RAW
            # Ensure it's plain postgresql:// (not asyncpg)
            url = url.replace("postgres://", "postgresql://", 1)
            url = url.replace("postgresql+asyncpg://", "postgresql://", 1)
            return url
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    JWT_SECRET_KEY: str = "change-me-to-a-random-secret-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # External APIs
    BMKG_API_URL: str = "https://data.bmkg.go.id/api/"
    BPS_API_URL: str = "https://webapi.bps.go.id/v1/"
    BPS_API_KEY: str = ""
    OSM_OVERPASS_URL: str = "https://overpass-api.de/api/interpreter"

    # Azure
    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_KEY: str = ""
    AZURE_OPENAI_DEPLOYMENT: str = "gpt-4o"

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    model_config = {"env_file": ".env", "env_prefix": "", "extra": "ignore"}


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
