"""Configuration for the Rijksmuseum adapter."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    postgres_dsn: str = "postgresql://nc:nc-dev-password@localhost:5432/nc"
    rijksmuseum_search_base_url: str = "https://data.rijksmuseum.nl/search/collection"
    rijksmuseum_oai_base_url: str = "https://data.rijksmuseum.nl/oai"
    rijksmuseum_iiif_image_base_url: str = "https://iiif.micr.io"
    rijksmuseum_change_discovery_url: str = "https://data.rijksmuseum.nl/cd/collection.json"
    rijksmuseum_fetch_timeout_seconds: int = 30
    rijksmuseum_requests_per_second: int = 2
    rijksmuseum_max_concurrency: int = 2
    rijksmuseum_dry_run: bool = True


settings = Settings()
