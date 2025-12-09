from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, \
    async_scoped_session

from src.client.storages.postgres.core import PostgresEngineProvider, \
    PostgresContextManager


class PostgresSessionProvider:
    def __init__(
        self,
        engine_creator: PostgresEngineProvider,
        context_manager: PostgresContextManager
    ):
        self._context_manager = context_manager
        self._session_factory = async_sessionmaker(
            bind=engine_creator.get_engine(),
            autocommit=False,
            autoflush=False,
        )
        self._scoped_session = async_scoped_session(
            session_factory=self._session_factory,
            scopefunc=self._context_manager.get_session_context,
        )

    def get_session(self) -> AsyncSession:
        """
        Creates and returns a new asynchronous session for PostgreSQL.
        """
        return self._scoped_session
