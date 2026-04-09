from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager


class IS3Connect(ABC):
    """
    Interface for a class that manages the connection to an S3-compatible storage
    service.

    Defines the contract for classes responsible for initializing and providing access
    to an S3 client instance using application settings.
    """

    @abstractmethod
    async def get_connect(self) -> AbstractAsyncContextManager:
        """
        Get the S3 client instance.

        :return: An S3 client instance for performing storage operations.
        """
        ...
