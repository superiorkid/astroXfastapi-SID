from pydantic import BaseSettings, PostgresDsn
from functools import lru_cache


class Settings(BaseSettings):
    database_url: PostgresDsn
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()