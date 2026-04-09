from abc import ABC, abstractmethod


class IS3Initializer(ABC):
    """
    Interface for a class that initializes S3 storage infrastructure.

    Defines the contract for classes responsible for setting up S3 buckets and
    configuring notification settings or other initialization routines required
    for proper S3 usage in the application.
    """

    @abstractmethod
    async def init(self) -> None:
        """
        Initialize the S3 storage infrastructure.

        This method should perform all necessary setup procedures, such as creating
        buckets and configuring notification settings.

        :return: None
        """
        ...
