from abc import ABC, abstractmethod
from contextlib import asynccontextmanager

from redis.asyncio import Redis as AIORedis
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session


class IPostgresSessionProvider(ABC):
    """
    Abstract interface for providing PostgreSQL async sessions.

    Implementations of this interface must return an active AsyncSession instance,
    typically used within a request lifecycle or a transactional scope.

    This abstraction helps decouple database access logic from concrete session
    creation, supporting better testability and adherence to the Dependency Inversion
    Principle.
    """

    @abstractmethod
    def get_session(self) -> AsyncSession:
        """Return current scoped AsyncSession."""
        ...


class IS3SessionProvider(ABC):
    """
    Interface for a class that provides S3 client sessions.

    Defines the contract for classes responsible for managing and providing access
    to S3 client sessions for performing storage operations.
    """

    @abstractmethod
    @asynccontextmanager
    async def get_session(self):
        """
        Get an S3 client session.

        :return: An S3 client instance for performing storage operations.
        """
        ...


class IRedisSessionProvider(ABC):
    """
    Abstract interface for providing Redis async client instances.

    Implementations of this interface must return a Redis client,
    which can be used to interact with Redis for caching, pub/sub,
    session storage, or token invalidation.

    This promotes flexibility and testability in components that rely on Redis.
    """

    @abstractmethod
    def get_client(self) -> AIORedis:
        """
        Retrieve an active Redis async client instance.

        :return: Instance of Redis async client for executing Redis operations.
        """
        ...
