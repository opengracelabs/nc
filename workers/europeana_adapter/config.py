"""Configuration for the Europeana adapter."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    postgres_dsn: str
    europeana_api_key: str = ""
    europeana_api_base_url: str = "https://api.europeana.eu/record/v2"
    europeana_requests_per_second: int = 2
    europeana_max_concurrency: int = 2
    europeana_fetch_timeout_seconds: int = 30
    europeana_dry_run: bool = True


settings = Settings()
