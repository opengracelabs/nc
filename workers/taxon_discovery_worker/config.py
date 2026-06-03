from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    postgres_dsn: str
    poll_interval_seconds: int = 30
    taxon_discovery_version: str = "1"
    taxon_discovery_top_limit: int = 50
    gbif_api_base_url: str = "https://api.gbif.org/v1"
    wikidata_sparql_endpoint: str = "https://query.wikidata.org/sparql"


settings = Settings()
