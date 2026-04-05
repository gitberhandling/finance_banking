"""Application configuration using pydantic-settings."""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Finance Backend API"


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
