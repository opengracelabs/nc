"""Configuration for the GBIF evidence-only adapter."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    gbif_api_base_url: str = "https://api.gbif.org/v1"
    gbif_page_size: int = 100
    gbif_occurrence_count_cap: int = 100
    gbif_fetch_timeout_seconds: int = 30
    gbif_user_agent: str = "opengrace-nc-gbif-evidence/1.0"
    gbif_dry_run: bool = True


SOURCE_SLUG = "gbif"
SCHEMA_STANDARD = "gbif_darwin_core_evidence_v1"
RIGHTS_POLICY_ID = "gbif_evidence_rights_matrix_v1"
API_BASE_URL = "https://api.gbif.org/v1"
USER_AGENT = "opengrace-nc-gbif-evidence/1.0"
OCCURRENCE_COUNT_CAP = 100

settings = Settings()

