"""Configuration for the Getty Museum Linked Art adapter."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    getty_collection_base_url: str = "https://data.getty.edu/museum/collection"
    getty_activity_stream_start_url: str = (
        "https://data.getty.edu/museum/collection/activity-stream/page/1"
    )
    getty_fetch_timeout_seconds: int = 30
    getty_user_agent: str = "NC-OpenGrace-Pipeline/1.0 (+https://opengrace.com)"
    getty_dry_run: bool = True


SOURCE_SLUG = "getty"
SCHEMA_STANDARD = "getty_linked_art_v1"
RIGHTS_POLICY_ID = "getty_rights_matrix_v1"

settings = Settings()

