"""Configuration for the Statens Museum for Kunst adapter."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    smk_api_base_url: str = "https://api.smk.dk/api/v1"
    smk_requests_per_second: int = 5
    smk_burst: int = 10
    smk_fetch_timeout_seconds: int = 30
    smk_page_limit: int = 100
    smk_max_rows: int = 2000
    smk_default_lang: str = "en"
    smk_user_agent: str = "NC-OpenGrace-Pipeline/1.0 (+https://opengrace.com)"
    smk_dry_run: bool = True


settings = Settings()

