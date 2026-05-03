from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from src.config.settings import Settings


class PostgresEngineProvider:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._engine = None

    def get_engine(self) -> AsyncEngine:
        if self._engine is None:
            self._engine = create_async_engine(url=self._settings.postgres.async_url)

        return self._engine
