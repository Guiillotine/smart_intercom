from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from src.config.settings import Settings


class PostgresEngineProvider:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._engine = None

    def get_engine(self) -> AsyncEngine:
        if self._engine is None:
            self._engine = create_async_engine(
                url=f"postgresql+asyncpg://{self._settings.POSTGRES.USER}"
                f":{self._settings.POSTGRES.PASSWORD}@{self._settings.POSTGRES.HOST}:"
                f"{self._settings.POSTGRES.PORT}"
                f"/{self._settings.POSTGRES.DB}"
            )

        return self._engine
