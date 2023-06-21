import os
from functools import lru_cache

from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    asyncpg_url: PostgresDsn = PostgresDsn.build(
        # scheme="postgresql+psycopg2",
        scheme="postgresql+asyncpg",
        user=os.getenv("POSTGRES_USER", "pguser"),
        password=os.getenv("POSTGRES_PASSWORD", "pgpass"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        path=f"/{os.getenv('POSTGRES_DB', 'users')}",
    )


@lru_cache
def get_settings():
    return Settings()

