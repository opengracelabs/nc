from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    postgres_dsn: str

    minio_endpoint: str = "localhost:9000"
    minio_access_key: str
    minio_secret_key: str
    minio_bucket_raw: str = "nc-raw"
    minio_secure: bool = False

    poll_interval_seconds: int = 30
    batch_size: int = 5
    bhl_page_image_url_template: str = (
        "https://www.biodiversitylibrary.org/pageimage/{bhl_page_id}"
    )
    fetch_timeout_seconds: int = 60
    fetch_max_bytes: int = 52_428_800


settings = Settings()
