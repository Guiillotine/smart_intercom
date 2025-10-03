from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from src.config.settings import Settings


class PostgresEngineCreator:
    def __init__(self, settings: Settings):
        self._settings = settings

    def get_engine(self) -> AsyncEngine:
        return create_async_engine(
            url=f"postgresql+asyncpg://{self._settings.POSTGRES.USER}"
            f":{self._settings.POSTGRES.PASSWORD}@{self._settings.POSTGRES.HOST}"
            f"/{self._settings.POSTGRES.DB}"
        )
