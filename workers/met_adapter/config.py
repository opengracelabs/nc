"""Configuration for the Metropolitan Museum of Art adapter."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    met_api_base_url: str = "https://collectionapi.metmuseum.org/public/collection/v1"
    met_requests_per_second: int = 5
    met_burst: int = 10
    met_fetch_timeout_seconds: int = 30
    met_user_agent: str = "NC-OpenGrace-Pipeline/1.0 (+https://opengrace.com)"
    met_dry_run: bool = True


settings = Settings()

