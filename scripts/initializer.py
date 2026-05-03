import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio

from src.config.settings.deps import get_settings
from src.client.storages.deps import get_postgres_session_provider
from src.client.storages.postgres.core import PostgresSessionContextManager
from src.client.storages.postgres.init.deps import get_postgres_initializer


class DatabasesInitializer:
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    @staticmethod
    async def _init_psql() -> None:
        """Initialize PostgreSQL database"""

        PostgresSessionContextManager.set_session_context(1)

        settings = get_settings()

        session_provider = get_postgres_session_provider(settings=settings)

        db = session_provider.get_session()

        psql_initializer = await get_postgres_initializer(db=db)

        await psql_initializer.init()
        await db.close()

        PostgresSessionContextManager.remove_session_context()

    async def _initialize(self) -> None:
        """Main initialization method"""

        self._logger.info("Creating initial data")
        await self._init_psql()
        self._logger.info("Initial data created")

    @classmethod
    async def run(cls) -> None:
        """Class method to run the initialization"""
        initializer = cls()
        await initializer._initialize()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    asyncio.run(DatabasesInitializer.run())
