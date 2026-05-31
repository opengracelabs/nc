from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    postgres_dsn: str

    minio_endpoint: str = "localhost:9000"
    minio_access_key: str
    minio_secret_key: str
    minio_bucket_raw: str = "nc-raw"
    minio_secure: bool = False

    unesco_api_key: str = ""
    wikidata_sparql_endpoint: str = "https://query.wikidata.org/sparql"
    wikimedia_user_agent: str = "NatureAndCulture/1.0 (opengracelabs@protonmail.com)"

    fetch_timeout_seconds: int = 60
    fetch_retry_max: int = 3
    discovery_auto_approve: bool = False
    unesco_replay_fixture: str = ""


settings = Settings()
