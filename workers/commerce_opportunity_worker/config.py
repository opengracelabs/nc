"""Commerce opportunity worker configuration."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_dsn: str = "postgresql://nc:nc-dev-password@localhost:5432/nc"
    batch_size: int = 25
    poll_interval_seconds: int = 60

    class Config:
        env_prefix = "NC_"


settings = Settings()
