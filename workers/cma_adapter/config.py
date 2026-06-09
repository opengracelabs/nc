"""Configuration for the Cleveland Museum of Art adapter."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    cma_api_base_url: str = "https://openaccess-api.clevelandart.org/api"
    cma_requests_per_second: int = 5
    cma_burst: int = 10
    cma_fetch_timeout_seconds: int = 30
    cma_page_limit: int = 100
    cma_max_limit: int = 1000
    cma_user_agent: str = "NC-OpenGrace-Pipeline/1.0 (+https://opengrace.com)"
    cma_dry_run: bool = True


settings = Settings()

