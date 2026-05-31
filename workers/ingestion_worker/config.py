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
    wikimedia_user_agent: str = "NatureAndCulture/1.0 (opengracelabs@protonmail.com)"

    fetch_timeout_seconds: int = 30
    fetch_retry_max: int = 3
    fetch_max_bytes: int = 52_428_800   # 50 MB default artifact cap

    poll_interval_seconds: int = 10
    worker_concurrency: int = 4


settings = Settings()
