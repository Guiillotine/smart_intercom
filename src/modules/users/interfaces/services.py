from abc import ABC, abstractmethod
from uuid import UUID

from src.modules.users.schemas import UserCreate, UserWithPassword, UserWithRole


class IUserSrv(ABC):
    """
    Interface for user service operations.

    Defines business operations for users.
    """

    @abstractmethod
    async def get_by_sid(self, sid: UUID) -> UserWithRole:
        """
        Get user by identifier.

        :param sid: User SID.
        :return: User data with role.
        """
        ...

    @abstractmethod
    async def get_by_email(self, email: str) -> UserWithPassword | None:
        """
        Get user by email.

        :param email: User email.
        :return: User data with password hash or None.
        """
        ...

    @abstractmethod
    async def create(self, user_in: UserCreate) -> UserWithRole:
        """
        Create user.

        :param user_in: User creation schema.
        :return: Created user data with role.
        """
        ...

    @staticmethod
    @abstractmethod
    def hash_password(password: str) -> str:
        """
        Hash plain password.

        :param password: Plain password string.
        :return: Password hash.
        """
        ...
