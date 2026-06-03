from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    postgres_dsn: str
    poll_interval_seconds: int = 30
    batch_size: int = 10
    research_version: str = "1"
    research_output_type: str = "place_brief"


settings = Settings()
