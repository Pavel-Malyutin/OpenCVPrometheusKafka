from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from recogniser.settings import get_settings

settings = get_settings()


Base = declarative_base()


class AsyncDatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    def init(self):
        print(f"2111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
        print(settings.asyncpg_url)
        print(f"2111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
        self._engine = create_async_engine(
            settings.asyncpg_url,
            future=True,
            echo=True,
        )
        self._session = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)()


db = AsyncDatabaseSession()
