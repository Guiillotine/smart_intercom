import logging

from redis.asyncio import Redis

from src.common.constants import ErrorCodesEnums
from src.common.interfaces import IBaseRedisRepo


class BaseRedisRepo(IBaseRedisRepo):
    """
    Concrete implementation of Redis repository operations.

    Provides asynchronous methods for basic Redis operations including
    get/set/delete operations with optional TTL support.
    """

    def __init__(
        self,
        redis: Redis,
        errors: ErrorCodesEnums,
        logger: logging.Logger,
    ):
        """
        Initialize Redis repository instance.

        :param redis: Configured Redis client instance
        :param errors: Error codes enumeration for exception handling
        :param logger: Configured logger instance for diagnostics
        """

        self._redis = redis
        self._errors = errors
        self._logger = logger

    async def set(self, key: str, value: str) -> None:
        """
        Store a string value by key in Redis without expiration.

        :param key: The key under which to store the value
        :param value: The string value to store
        """

        await self._redis.set(name=key, value=value)

    async def get(self, key: str) -> str | None:
        """
        Retrieve a string value by key from Redis.

        :param key: The key to retrieve
        :return: The stored dict value or None if key doesn't exist
        """

        raw_value = await self._redis.get(name=key)

        if not raw_value:
            return None

        return raw_value

    async def delete(self, key: str) -> int:
        """
        Remove a key from Redis.

        :param key: The key to remove
        :return: Number of keys actually deleted (1 or 0)
        """

        return await self._redis.delete(key)

    async def delete_by_prefix(self, prefix: str):
        """
        Asynchronously delete all Redis keys that start with the given prefix.

        :param prefix: The prefix string to filter keys for deletion.
        """

        cursor = b"0"
        pattern = f"{prefix}*"

        while cursor:
            cursor, keys = await self._redis.scan(
                cursor=cursor,
                match=pattern,
                count=50,
            )
            if keys:
                await self._redis.delete(*keys)
            if cursor == b"0":
                break

    async def exists(self, key: str) -> bool:
        """
        Check if a key exists in Redis.

        :param key: The key to check
        :return: True if key exists, False otherwise
        """

        return await self._redis.exists(key) > 0

    async def set_with_ttl(self, key: str, value: str, ttl: int) -> None:
        """
        Store a string value by key in Redis with expiration time.

        :param key: The key under which to store the value
        :param value: The string value to store
        :param ttl: Time-to-live in seconds until key expiration
        """

        await self._redis.setex(name=key, time=ttl, value=value)
