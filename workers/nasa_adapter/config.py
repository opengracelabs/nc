"""Configuration for the NASA Image and Video Library adapter."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    nasa_images_api_base_url: str = "https://images-api.nasa.gov"
    nasa_images_fetch_timeout_seconds: int = 30
    nasa_images_page_size: int = 100
    nasa_images_user_agent: str = "NC-OpenGrace-Pipeline/1.0 (+https://opengrace.com)"
    nasa_images_dry_run: bool = True


SOURCE_SLUG = "nasa_images"
SCHEMA_STANDARD = "nasa_images_collection_json_v1"
RIGHTS_POLICY_ID = "nasa_images_rights_class_10_v1"
API_BASE_URL = "https://images-api.nasa.gov"
USER_AGENT = "NC-OpenGrace-Pipeline/1.0 (+https://opengrace.com)"
IMAGES_API_HOST = "images-api.nasa.gov"
EXCLUDED_API_HOST = "api.nasa.gov"

settings = Settings()
