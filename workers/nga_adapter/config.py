"""Configuration for the National Gallery of Art Open Data adapter."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    nga_opendata_base_url: str = (
        "https://raw.githubusercontent.com/NationalGalleryOfArt/opendata/main/data"
    )
    nga_fetch_timeout_seconds: int = 30
    nga_user_agent: str = "NC-OpenGrace-Pipeline/1.0 (+https://opengrace.com)"
    nga_dry_run: bool = True


settings = Settings()
