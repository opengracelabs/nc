"""Configuration for the Minneapolis Institute of Art adapter."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    mia_api_base_url: str = "https://search.artsmia.org"
    mia_image_url_template: str = "https://{shard}.api.artsmia.org/800/{object_id}.jpg"
    mia_fetch_timeout_seconds: int = 30
    mia_user_agent: str = "NC-OpenGrace-Pipeline/1.0 (+https://opengrace.com)"
    mia_dry_run: bool = True


SOURCE_SLUG = "mia"
SCHEMA_STANDARD = "mia_collection_json_v1"
RIGHTS_POLICY_ID = "mia_rights_matrix_v2"
METADATA_LICENSE_URI = "https://creativecommons.org/publicdomain/zero/1.0/"

settings = Settings()
