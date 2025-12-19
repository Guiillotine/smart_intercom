from typing import Annotated, AsyncGenerator

from fastapi import Depends

from src.client.storages import PostgresSessionProvider
from src.client.storages.postgres.core.deps import get_psql_context_manager, \
    get_psql_engine_provider


def get_postgres_session_provider() -> PostgresSessionProvider:
    """
    Construct and return an instance of PostgresSessionProvider.

    Initializes a PostgresSessionProvider with a session context manager, allowing it
    to provide context-aware PostgreSQL sessions.
    """
    return PostgresSessionProvider(
        engine_creator=get_psql_engine_provider(),
        context_manager=get_psql_context_manager(),
    )


async def get_db(
    session_provider: Annotated[
        PostgresSessionProvider, Depends(get_postgres_session_provider)
    ],
) -> AsyncGenerator:
    """
    Provides a PostgreSQL database session.

    The session is automatically closed after the request lifecycle.
    """
    db = session_provider.get_session()
    try:
        yield db
    finally:
        await db.close()
