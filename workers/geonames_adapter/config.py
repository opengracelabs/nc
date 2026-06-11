"""Configuration for the GeoNames place identity adapter."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    geonames_api_base_url: str = "http://api.geonames.org"
    geonames_username: str | None = None
    geonames_page_size: int = 10
    geonames_fetch_timeout_seconds: int = 30
    geonames_cache_ttl_days: int = 90


SOURCE_NAME = "geonames"
SOURCE_ROLE = "place_identity"
SCHEMA_STANDARD = "geonames_place_identity_evidence_v1"
RIGHTS_POLICY_ID = "geonames_attribution_policy_v1"
API_VERSION = "geonames_api_v1"
GEONAMES_BASE_URL = "https://www.geonames.org"
CC_BY_4_URI = "https://creativecommons.org/licenses/by/4.0/"
ATTRIBUTION_SHORT = "Geographic data (c) GeoNames (geonames.org) - CC BY 4.0"

settings = Settings()

