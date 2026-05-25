from abc import ABC, abstractmethod

from src.common.interfaces import IPostgresBaseRepo, IBaseRedisRepo
from src.modules.users.models import RoleModel, UserModel
from src.modules.users.schemas import RoleCreate, RoleUpdate, UserUpdate, UserCreateInDB


class IRolePostgresRepo(IPostgresBaseRepo[RoleModel, RoleCreate, RoleUpdate], ABC):
    """
    Interface for user role PostgreSQL repository operations.

    Extends base PostgreSQL repository with the role model contract.
    """


class IUserPostgresRepo(IPostgresBaseRepo[UserModel, UserCreateInDB, UserUpdate], ABC):
    """
    Interface for user PostgreSQL repository operations.

    Extends base PostgreSQL repository with user-specific queries.
    """

    @abstractmethod
    async def get_by_email(self, email: str) -> UserModel | None:
        """
        Get user database model by email.

        :param email: User email.
        :return: User database model or None.
        """
        ...


class IAuthRedisRepo(IBaseRedisRepo, ABC):
    """
    Abstract interface for authentication-related Redis operations.

    Extends the base Redis repository with methods specific to storing
    and managing verification data used in the authentication process.
    """
    pass