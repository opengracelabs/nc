from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    postgres_dsn: str
    poll_interval_seconds: int = 30
    batch_size: int = 10
    extraction_timeout_seconds: int = 300
    extraction_version: str = "1"
    rescore_interval_days: int = 7


settings = Settings()
