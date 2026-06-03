from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    postgres_dsn: str
    poll_interval_seconds: int = 30
    batch_size: int = 10
    bhl_api_base_url: str = "https://www.biodiversitylibrary.org/api3"
    bhl_api_key: str | None = None


settings = Settings()
