from abc import ABC, abstractmethod

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from src.modules.users.schemas import LoginToken, RefreshToken, UserCreate


class IAuthCtrl(ABC):
    """
    Interface for authentication-related route definitions.

    This abstract base class defines the contract for authentication routers,
    ensuring consistent implementation of auth-related endpoints across different
    authentication providers or implementations.
    """

    @property
    @abstractmethod
    def controller(self) -> APIRouter:
        """
        Returns the FastAPI router with all registered authentication endpoints.

        :return: Configured APIRouter instance containing auth routes.
        """
        ...

    @staticmethod
    @abstractmethod
    async def login(
        form_data: OAuth2PasswordRequestForm, auth_service: IAuthUC, user_agent: str
    ) -> LoginToken:
        """
        Authenticate user using form credentials and return a token pair.

        :param form_data: Login form data (username and password).
        :param user_agent: The User-Agent string from the client request.
        :param auth_service: Authentication use case instance.
        :return: JWT access and refresh tokens.
        """
        ...

    @staticmethod
    @abstractmethod
    async def logout(
        token: str,
        auth_usecase: IAuthUC,
        everywhere: bool,
    ) -> JSONResponse:
        """
        Log out the user by invalidating tokens.

        :param token: Access or refresh token to invalidate.
        :param auth_usecase: Authentication use case instance containing business logic.
        :param everywhere: If True, log out from all sessions; otherwise, current
                session only.
        :return: JSON response confirming successful logout.
        """
        ...

    @staticmethod
    @abstractmethod
    async def update_access_token(
        body: RefreshToken,
        user_agent: str,
        auth_usecase: IAuthUC,
    ) -> LoginToken:
        """
        Refresh the access token using a valid refresh token.

        :param body: RefreshToken instance containing the refresh token data.
        :param user_agent: The User-Agent string from the client request.
        :param auth_usecase: Authentication use case instance containing business logic.
        :return: New login tokens including access and refresh tokens.
        """
        ...

    @staticmethod
    @abstractmethod
    async def register(
        user_in: UserCreate,
        user_agent: str,
        auth_usecase: IAuthUC,
    ) -> LoginToken:
        """
        Register a new user in the system.

        :param user_in: UserCreate schema containing the data for the new user.
        :param user_agent: The User-Agent string from the client request.
        :param auth_usecase: Use case handler for authentication operations.
        :return: CreatedUser instance representing the newly registered user.
        """
        ...
