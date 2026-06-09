"""Configuration for the Walters Art Museum Open Data adapter."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    walters_opendata_base_url: str = (
        "https://raw.githubusercontent.com/WaltersArtMuseum/api-thewalters-org/main"
    )
    walters_fetch_timeout_seconds: int = 30
    walters_user_agent: str = "NC-OpenGrace-Pipeline/1.0 (+https://opengrace.com)"
    walters_dry_run: bool = True


settings = Settings()
