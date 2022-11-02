from functools import lru_cache
from pydantic import BaseSettings, PostgresDsn
from databases import Database


class Settings(BaseSettings):
    debug: bool = False
    database_url: PostgresDsn = 'postgres://user:password@host:1234/database'
    log_file: str = 'stdout'

    class Config():
        env_file = '.env'


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_database() -> Database:
    settings = get_settings()
    return Database(settings.database_url)
