"""Configuration constants for the NOAA discovery-only adapter."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    noaa_flickr_api_base_url: str = "https://api.flickr.com/services/rest/"
    noaa_flickr_default_user_id: str = "usoceangov"
    noaa_fetch_timeout_seconds: int = 30
    noaa_page_size: int = 100
    noaa_user_agent: str = "opengrace-nc-noaa-discovery/1.0"
    noaa_dry_run: bool = True


SOURCE_SLUG = "noaa"
SCHEMA_STANDARD = "noaa_discovery_v1"
RIGHTS_POLICY_ID = "noaa_rights_matrix_v1"
FLICKR_API_BASE_URL = "https://api.flickr.com/services/rest/"
FLICKR_PHOTO_PAGE_BASE_URL = "https://www.flickr.com/photos"
PHOTOLIB_BASE_URL = "https://photolib.noaa.gov"
USER_AGENT = "opengrace-nc-noaa-discovery/1.0"
DEFAULT_FLICKR_USER_ID = "usoceangov"

settings = Settings()

