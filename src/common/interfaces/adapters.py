from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from httpx import Response
from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy.sql.base import ExecutableOption

from src.common.schemas.core_schema import SQLFilterBase

if TYPE_CHECKING:
    from src.common.models import CoreModel

ModelType = TypeVar("ModelType", bound="CoreModel")
CreateSchemaType = TypeVar("CreateSchemaType", bound=PydanticBaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=PydanticBaseModel)


class IPostgresBaseRepo[ModelType, CreateSchemaType, UpdateSchemaType](ABC):
    """
    Abstract interface for generic CRUD operations on a SQLAlchemy model.
    """

    @abstractmethod
    async def get_by_sid(
        self, sid: UUID, custom_options: tuple[ExecutableOption, ...] = None
    ) -> ModelType | None:
        """
        Retrieve a single record by its unique SID.

        :param sid: Unique identifier.
        :param custom_options: Optional SQLAlchemy loader options.
        :return: A single model instance or None.
        """
        ...

    @abstractmethod
    async def get_all(
        self,
        filters: SQLFilterBase = None,
        custom_options: tuple[ExecutableOption, ...] = None,
    ) -> Sequence[ModelType]:
        """
        Retrieve all records for the model.

        :param custom_options: Optional SQLAlchemy query options.
        :param filters: Optional FastApi SQLAlchemy model filters.
        :return: List of all model instances.
        """

        ...

    @abstractmethod
    async def create(
        self, obj_in: CreateSchemaType, with_commit: bool = True
    ) -> ModelType:
        """
        Create a new record in the database.

        :param obj_in: Input schema instance.
        :param with_commit: Whether to immediately commit the transaction.
        :return: The newly created model instance.
        """
        ...

    @abstractmethod
    async def update(
        self,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
        with_commit: bool = True,
    ) -> ModelType:
        """
        Update an existing record with new data.

        :param db_obj: The current persisted model instance.
        :param obj_in: Updated data as dict or schema.
        :param with_commit: Whether to commit the transaction.
        :return: Updated model instance.
        """
        ...

    @abstractmethod
    async def delete(self, sid: UUID, with_commit: bool = True) -> ModelType | None:
        """
        Delete a record by its unique SID.

        :param sid: Unique identifier of the object to delete.
        :param with_commit: Whether to commit the transaction after deletion.
        :return: The deleted model instance or None.
        """
        ...


class IS3BaseRepo(ABC):
    """
    Interface for a repository class that provides basic S3 object operations.

    Defines the contract for classes responsible for interacting with S3-compatible
    storage: getting, putting, deleting, and listing objects in buckets.
    """

    @abstractmethod
    async def get_object(self, bucket: str, key: str) -> bytes:
        """
        Retrieve an object from the specified S3 bucket.

        :param bucket: The name of the S3 bucket.
        :param key: The key (path/filename) of the object in the bucket.
        :return: The object's data as bytes.
        """
        ...

    @abstractmethod
    async def put_object(self, bucket: str, key: str, data: bytes) -> str:
        """
        Upload an object to the specified S3 bucket.

        :param bucket: The name of the S3 bucket.
        :param key: The key (path/filename) to assign to the object.
        :param data: The object's data as bytes.
        :return: key
        """
        ...

    @abstractmethod
    async def delete_object(self, bucket: str, key: str) -> None:
        """
        Delete an object from the specified S3 bucket.

        :param bucket: The name of the S3 bucket.
        :param key: The key (path/filename) of the object to delete.
        :return: None
        """
        ...

    @abstractmethod
    async def list_objects(
        self, bucket: str, prefix: str | None = None
    ) -> Sequence[str]:
        """
        List objects in the specified S3 bucket, optionally filtering by prefix.

        :param bucket: The name of the S3 bucket.
        :param prefix: Optional prefix to filter objects.
        :return: A sequence of object keys (filenames/paths) as strings.
        """
        ...


class IBaseRedisRepo(ABC):
    """Abstract base interface for Redis repository operations."""

    @abstractmethod
    async def set(self, key: str, value: str) -> None:
        """
        Store a string value by key in Redis without expiration.

        :param key: The key under which to store the value
        :param value: The string value to store
        """
        ...

    @abstractmethod
    async def get(self, key: str) -> str | None:
        """
        Retrieve a string value by key from Redis.

        :param key: The key to retrieve
        :return: The stored dict value or None if key doesn't exist
        """
        ...

    @abstractmethod
    async def delete(self, key: str) -> int:
        """
        Remove a key from Redis.

        :param key: The key to remove
        :return: 1 if key was deleted, 0 if it didn't exist
        """
        ...

    @abstractmethod
    async def delete_by_prefix(self, prefix: str):
        """
        Delete all Redis keys that start with the given prefix.

        :param prefix: The prefix string to filter keys for deletion.
        """

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """
        Check if a key exists in Redis.

        :param key: The key to check
        :return: True if key exists, False otherwise
        """
        ...

    @abstractmethod
    async def set_with_ttl(self, key: str, value: str, ttl: int) -> None:
        """
        Store a string value by key in Redis with expiration time.

        :param key: The key under which to store the value
        :param value: The string value to store
        :param ttl: Time-to-live in seconds until key expiration
        """
        ...
