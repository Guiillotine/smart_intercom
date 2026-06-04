from abc import ABC, abstractmethod
from uuid import UUID

from fastapi.security import OAuth2PasswordRequestForm

from src.common.schemas import Msg
from src.modules.users.schemas import (
    LoginToken,
    UserCreate,
    UserCreateByAdmin,
    UserWithRole,
)


class IUserUC(ABC):
    """
    Interface for user use case operations.

    Defines application-level user workflows.
    """

    @abstractmethod
    async def get_user_info(self, user_sid: UUID) -> UserWithRole:
        """
        Get current user information.

        :param user_sid: Current authorized user SID.
        :return: User data with role.
        """
        ...

    @abstractmethod
    async def get_by_sid(self, sid: UUID, user_sid: UUID) -> UserWithRole:
        """
        Get user by identifier.

        :param sid: Target user SID.
        :param user_sid: Current authorized user SID.
        :return: User data with role.
        """
        ...


class IAuthUC(ABC):
    """
    Interface for auth use case operations.

    Defines application-level authentication workflows.
    """

    @abstractmethod
    async def get_token_pair(
        self, form_data: OAuth2PasswordRequestForm,
    ) -> LoginToken:
        """
        Generates a pair of access and refresh tokens for the user based on provided
        credentials.

        :param form_data: The form data containing the username and password.
        :return: A LoginToken instance containing the generated tokens.
        """
        ...

    @abstractmethod
    async def register(
        self, user_in: UserCreate,
    ) -> LoginToken:
        """
        Register a user and create token pair.

        :param user_in: User registration schema.
        :return: Access and refresh token pair.
        """
        ...

    @abstractmethod
    async def register_by_admin(
        self,
        user_in: UserCreateByAdmin,
        admin_user_sid: UUID,
    ) -> UserWithRole:
        """
        Register a user with an explicit role by an authorized administrator.

        :param user_in: User registration schema with role.
        :param admin_user_sid: Current administrator SID.
        :return: Created user data with role.
        """
        ...

    @abstractmethod
    async def update_access_token(
        self, refresh_token: str,
    ) -> LoginToken:
        """
        Refresh access token using refresh token.

        :param refresh_token: Refresh token string.
        :return: New access and refresh token pair.
        """
        ...

    @abstractmethod
    async def delete_token(self, token: str) -> Msg:
        """
        Delete or invalidate user token.

        :param token: Current bearer token.
        :return: Operation result message.
        """
        ...

    @abstractmethod
    async def register_by_admin(
        self,
        user_in: UserCreateByAdmin,
        admin_user_sid: UUID,
    ) -> UserWithRole:
        """
        Register a user with an explicit role by an authorized administrator.

        :param user_in: User registration schema with role.
        :param admin_user_sid: Current administrator SID.
        :return: Created user data with role.
        """
        ...
