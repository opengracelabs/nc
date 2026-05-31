from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    postgres_dsn: str

    minio_endpoint: str = "localhost:9000"
    minio_access_key: str
    minio_secret_key: str
    minio_bucket_raw: str = "nc-raw"
    minio_bucket_normalized: str = "nc-normalized"
    minio_secure: bool = False

    poll_interval_seconds: int = 10
    batch_size: int = 5
    preservation_timeout_seconds: int = 300


settings = Settings()
