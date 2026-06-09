"""Configuration for the Art Institute of Chicago adapter."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    aic_api_base_url: str = "https://api.artic.edu/api/v1"
    aic_requests_per_second: int = 5
    aic_burst: int = 10
    aic_fetch_timeout_seconds: int = 30
    aic_page_limit: int = 100
    aic_user_agent: str = "NC-OpenGrace-Pipeline/1.0 (+https://opengrace.com)"
    aic_dry_run: bool = True


settings = Settings()

