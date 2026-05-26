from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, \
    async_scoped_session
from redis.asyncio import Redis as AIORedis

from src.client.interfaces import IRedisSessionProvider, IS3SessionProvider, \
    IPostgresSessionProvider
from src.client.storages.postgres.core import PostgresEngineProvider, \
    PostgresSessionContextManager
from src.client.storages.s3.interfaces import IS3Connect
from src.config.settings import Settings


class PostgresSessionProvider(IPostgresSessionProvider):
    def __init__(
        self,
        engine_creator: PostgresEngineProvider,
        context_manager: PostgresSessionContextManager
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
        """Return current scoped AsyncSession."""
        session: AsyncSession = self._scoped_session() # TODO: проверить, меняла

        return session


class S3SessionProvider(IS3SessionProvider):
    """
    Provides functionality for managing and retrieving S3 sessions.
    Utilizes the specified S3 client to establish and return asynchronous connections
    to the S3 storage service.
    """

    def __init__(self, s3_client: IS3Connect):
        """
        Initialize the S3SessionProvider with a given S3 client.

        :param s3_client: Instance of S3Connect used to manage S3 connections.
        """

        self._s3_client = s3_client

    @asynccontextmanager
    async def get_session(self):
        """
        Retrieve an active S3 session using the configured S3 client.

        :return: An active asynchronous S3 session.
        """

        cm = await self._s3_client.get_connect()
        async with cm as client:
            yield client


class RedisSessionProvider(IRedisSessionProvider):
    """
    RedisSessionProvider is responsible for providing Redis async client connections.

    This class implements the IRedisSessionProvider interface. It provides methods
    to create and return Redis client connections for interacting with the Redis store.
    """

    def __init__(self, settings: Settings):
        """
        Initializes the RedisSessionProvider with a Redis async client instance.
        """

        self._settings = settings
        self._client = AIORedis(
            host=self._settings.redis.HOST,
            port=self._settings.redis.PORT,
            decode_responses=True,
        )

    def get_client(self) -> AIORedis:
        """
        Returns the Redis async client instance.

        :return: A Redis client instance to interact with Redis.
        """

        return self._client
