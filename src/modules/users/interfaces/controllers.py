from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from src.modules.users.interfaces.usecases import IAuthUC, IUserUC
from src.modules.users.schemas import (
    LoginToken,
    RefreshToken,
    UserCreate,
    UserCreateByAdmin,
    UserWithRole,
)


class IAuthCtrl(ABC):
    """
    Interface for authentication controller operations.

    Defines the contract for authentication-related API endpoints.
    """

    @property
    @abstractmethod
    def controller(self) -> APIRouter:
        """
        Get the configured APIRouter instance.

        :return: Configured FastAPI router with auth routes.
        """
        ...

    @staticmethod
    @abstractmethod
    async def login(
        form_data: OAuth2PasswordRequestForm,
        auth_usecase: IAuthUC,
    ) -> LoginToken:
        """
        Authenticate user and return token pair.

        :param form_data: OAuth2 password form data.
        :param auth_usecase: Auth use case dependency.
        :return: Access and refresh token pair.
        """
        ...

    @staticmethod
    @abstractmethod
    async def logout(
        token: str,
        auth_usecase: IAuthUC,
    ) -> JSONResponse:
        """
        Log out user by invalidating token data.

        :param token: Current bearer token.
        :param auth_usecase: Auth use case dependency.
        :return: JSON response with operation result.
        """
        ...

    @staticmethod
    @abstractmethod
    async def update_access_token(
        auth_usecase: IAuthUC,
        body: RefreshToken,
    ) -> LoginToken:
        """
        Refresh access token.

        :param auth_usecase: Auth use case dependency.
        :param body: Refresh token request body.
        :return: New access and refresh token pair.
        """
        ...

    @staticmethod
    @abstractmethod
    async def register(
        user_in: UserCreate,
        auth_usecase: IAuthUC,
    ) -> LoginToken:
        """
        Register a user and return token pair.

        :param user_in: User registration schema.
        :param auth_usecase: Auth use case dependency.
        :return: Access and refresh token pair.
        """
        ...

    @staticmethod
    @abstractmethod
    async def register_by_admin(
        user_in: UserCreateByAdmin,
        admin_user_sid: UUID,
        auth_usecase: IAuthUC,
    ) -> UserWithRole:
        """
        Register a user with an explicit role by an administrator.

        :param user_in: User registration schema with role.
        :param admin_user_sid: Current administrator SID.
        :param auth_usecase: Auth use case dependency.
        :return: Created user data with role.
        """
        ...


class IUserCtrl(ABC):
    """
    Interface for user controller operations.

    Defines the contract for user-related API endpoints.
    """

    @property
    @abstractmethod
    def controller(self) -> APIRouter:
        """
        Get the configured APIRouter instance.

        :return: Configured FastAPI router with user routes.
        """
        ...

    @staticmethod
    @abstractmethod
    async def me(user_sid: UUID, user_usecase: IUserUC) -> UserWithRole:
        """
        Get current user information.

        :param user_sid: Current authorized user SID.
        :param user_usecase: User use case dependency.
        :return: Current user data with role.
        """
        ...

    @staticmethod
    @abstractmethod
    async def get_user(
        sid: UUID, user_sid: UUID, user_usecase: IUserUC
    ) -> UserWithRole:
        """
        Get user information by identifier.

        :param sid: Target user SID.
        :param user_sid: Current authorized user SID.
        :param user_usecase: User use case dependency.
        :return: User data with role.
        """
        ...
