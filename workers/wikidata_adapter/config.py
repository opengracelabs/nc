"""Configuration for the Wikidata identity/evidence adapter."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    wikidata_api_base_url: str = "https://www.wikidata.org/w/api.php"
    wikidata_fetch_timeout_seconds: int = 30
    wikidata_user_agent: str = "opengrace-nc-wikidata-evidence/1.0"
    wikidata_default_language: str = "en"
    wikidata_cache_ttl_days: int = 30


SOURCE_NAME = "wikidata"
SOURCE_ROLE = "context_only"
SCHEMA_STANDARD = "wikidata_identity_evidence_v1"
RIGHTS_POLICY_ID = "wikidata_evidence_policy_v1"
WIKIDATA_ENTITY_BASE_URL = "https://www.wikidata.org/wiki"
USER_AGENT = "opengrace-nc-wikidata-evidence/1.0"

settings = Settings()

