"""Configuration for the National Archives Catalog adapter."""
from __future__ import annotations

import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    nara_api_base_url: str = "https://catalog.archives.gov/api/v2"
    nara_fetch_timeout_seconds: int = 30
    nara_page_limit: int = 25
    nara_user_agent: str = "NC-OpenGrace-Pipeline/1.0 (+https://opengrace.com)"
    nara_dry_run: bool = True


SOURCE_SLUG = "nara"
SCHEMA_STANDARD = "nara_catalog_v2"
RIGHTS_POLICY_ID = "nara_rights_matrix_v1"
API_KEY_ENV = "NARA_API_KEY"

settings = Settings()


def get_api_key() -> str | None:
    """Return the NARA API key from the process environment only."""
    value = os.getenv(API_KEY_ENV)
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None

