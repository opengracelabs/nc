"""Configuration for the Gallica adapter."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    gallica_base_url: str = "https://gallica.bnf.fr"
    gallica_oai_base_url: str = "https://oai.bnf.fr/oai2/OAIHandler"
    gallica_fetch_timeout_seconds: int = 30
    gallica_requests_per_second: int = 2
    gallica_max_concurrency: int = 2
    gallica_dry_run: bool = True


settings = Settings()

