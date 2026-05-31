from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    nc_env: str = "development"
    nc_secret_key: str

    postgres_dsn: str

    minio_endpoint: str = "localhost:9000"
    minio_access_key: str
    minio_secret_key: str
    minio_bucket_raw: str = "nc-raw"
    minio_bucket_normalized: str = "nc-normalized"
    minio_bucket_curated: str = "nc-curated"
    minio_secure: bool = False

    redis_url: str = "redis://localhost:6379/0"


settings = Settings()
