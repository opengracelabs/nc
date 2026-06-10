"""Configuration for the Yale LUX Linked Art adapter."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    yale_lux_base_url: str = "https://lux.collections.yale.edu"
    yale_manifest_base_url: str = "https://manifests.collections.yale.edu"
    yale_fetch_timeout_seconds: int = 30
    yale_page_length: int = 20
    yale_user_agent: str = "NC-OpenGrace-Pipeline/1.0 (+https://opengrace.com)"
    yale_dry_run: bool = True


settings = Settings()

