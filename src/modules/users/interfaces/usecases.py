from abc import ABC, abstractmethod
from uuid import UUID

from fastapi.security import OAuth2PasswordRequestForm

from src.common.schemas import Msg
from src.modules.users.constants.enums import LogoutType
from src.modules.users.schemas import LoginToken, UserCreate, UserWithRole


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
        self, form_data: OAuth2PasswordRequestForm, user_agent: str | None = None
    ) -> LoginToken:
        """
        Authenticate user and create token pair.

        :param form_data: OAuth2 password form data.
        :param user_agent: Optional User-Agent request header.
        :return: Access and refresh token pair.
        """
        ...

    @abstractmethod
    async def register(
        self, user_in: UserCreate, user_agent: str | None = None
    ) -> LoginToken:
        """
        Register a user and create token pair.

        :param user_in: User registration schema.
        :param user_agent: Optional User-Agent request header.
        :return: Access and refresh token pair.
        """
        ...

    @abstractmethod
    async def update_access_token(
        self, refresh_token: str, user_agent: str | None = None
    ) -> LoginToken:
        """
        Refresh access token using refresh token.

        :param refresh_token: Refresh token string.
        :param user_agent: Optional User-Agent request header.
        :return: New access and refresh token pair.
        """
        ...

    @abstractmethod
    async def delete_tokens(self, token: str, logout_type: LogoutType) -> Msg:
        """
        Delete or invalidate user tokens.

        :param token: Current bearer token.
        :param logout_type: Logout scope.
        :return: Operation result message.
        """
        ...
