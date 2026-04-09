from typing import Annotated, AsyncGenerator

from fastapi import Depends
from redis.asyncio import Redis as AIORedis

from src.client.interfaces import IS3SessionProvider
from src.client.storages import PostgresSessionProvider
from src.client.storages.postgres.core.deps import get_psql_session_context_manager, \
    get_psql_engine_provider
from src.client.storages.s3.core.deps import get_s3_client
from src.client.storages.s3.interfaces import IS3Connect
from src.client.storages.session import S3SessionProvider, RedisSessionProvider
from src.config.settings import Settings
from src.config.settings.deps import get_settings


def get_postgres_session_provider(
    settings: Annotated[Settings, Depends(get_settings)],
) -> PostgresSessionProvider:
    """
    Construct and return an instance of PostgresSessionProvider.

    Initializes a PostgresSessionProvider with a session context manager, allowing it
    to provide context-aware PostgreSQL sessions.
    """
    return PostgresSessionProvider(
        engine_creator=get_psql_engine_provider(settings=settings),
        context_manager=get_psql_session_context_manager(),
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


async def get_s3_session_provider(
    s3_client: Annotated[IS3Connect, Depends(get_s3_client)],
) -> IS3SessionProvider:
    """
    Create and return an S3SessionProvider instance using the provided S3 client.

    :param s3_client: Instance of IS3Connect used to manage S3 connections.
    :return: S3SessionProvider instance.
    """

    return S3SessionProvider(s3_client=s3_client)


async def get_redis_session_provider(
    settings: Annotated[Settings, Depends(get_settings)],
) -> RedisSessionProvider:
    """
    Returns an instance of the RedisSessionProvider.

    This provider is responsible for creating and managing Redis client sessions.

    :return: An instance of RedisSessionProvider.
    """

    return RedisSessionProvider(settings=settings)


async def get_redis_client(
    session_provider: Annotated[
        RedisSessionProvider,
        Depends(get_redis_session_provider),
    ],
) -> AsyncGenerator[AIORedis, None]:
    """
    Provides a Redis client session.

    This dependency can be used to inject a Redis client into FastAPI routes or
    services that need to interact with Redis.

    Redis clients are typically long-lived, and this dependency ensures that the client
    is available throughout the request lifecycle.

    :param session_provider: The provider responsible for providing Redis client
            sessions.
    :return: A Redis client instance.
    """

    redis_client = session_provider.get_client()
    try:
        yield redis_client
    finally:
        pass
