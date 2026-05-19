from typing import Annotated

from fastapi import APIRouter, Depends, Header, Query
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.responses import JSONResponse

from src.common.deps.oauth_scheme import oauth2_scheme
from src.common.schemas import Msg
from src.modules.users.constants.enums import LogoutType
from src.modules.users.interfaces import IAuthCtrl
from src.modules.users.schemas import LoginToken, RefreshToken, UserCreate


class AuthCtrl(IAuthCtrl):
    """
    Routing class for authentication-related API endpoints.

    This class is responsible for configuring and registering routes related
    to authentication workflows such as login, logout, token refresh, and user
    registration.
    """

    def __init__(
        self,
        enums: AuthCtrlEnums,
    ):
        """
        Initializes the AuthRouters instance.

        Sets up an internal FastAPI APIRouter and binds all authentication-related
        routes.
        """

        self._controller = APIRouter()
        self._enums = enums
        self._add_controllers()

    @property
    def controller(self) -> APIRouter:
        """
        Returns the FastAPI router instance with all registered authentication
        endpoints.

        :return: Configured APIRouter for inclusion in the main FastAPI application.
        """

        return self._controller

    def _add_controllers(self) -> None:
        """
        Registers all authentication-related routes to the internal router instance.
        """

        self._controller.add_api_route(
            path=self._enums.CtrlPath.login,
            endpoint=self.login,
            methods=[self._enums.Common.RequestTypes.POST],
            response_model=LoginToken,
        )
        self._controller.add_api_route(
            path=self._enums.CtrlPath.logout,
            endpoint=self.logout,
            methods=[self._enums.Common.RequestTypes.POST],
            response_model=Msg,
        )
        self._controller.add_api_route(
            path=self._enums.CtrlPath.refresh_token,
            endpoint=self.update_access_token,
            methods=[self._enums.Common.RequestTypes.POST],
            response_model=LoginToken,
        )
        self._controller.add_api_route(
            path=self._enums.CtrlPath.register,
            endpoint=self.register,
            methods=[self._enums.Common.RequestTypes.POST],
            response_model=LoginToken,
        )

    @staticmethod
    async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        auth_usecase: Annotated[IAuthUC, Depends(get_auth_usecase)],
        user_agent: Annotated[str | None, Header(alias="User-Agent")] = None,
    ) -> LoginToken:
        """
        Authenticate user and return JWT token pair.

        ## Parameters:
        - **email**: User's email identifier
        - **password**: User's password (plaintext)

        ## Returns:
        - **accessToken**: JWT access token for API authorization
        - **refreshToken**: JWT token for obtaining new access tokens

        ## Notes:
        - Implements OAuth2 password grant flow
        - Tokens should be used with 'Authorization: Bearer <token>' header
        """

        return await auth_usecase.get_token_pair(
            form_data=form_data, user_agent=user_agent
        )

    @staticmethod
    async def logout(
        token: Annotated[str, Depends(oauth2_scheme)],
        auth_usecase: Annotated[IAuthUC, Depends(get_auth_usecase)],
        logout_type: LogoutType = Query(LogoutType.current, alias="logoutType"),
    ) -> JSONResponse:
        """
        Log out the user by invalidating their token(s).

        ## Parameters:
        - **token**: Access or refresh token to be invalidated, extracted from the
                request.
        - **auth_usecase**: Authentication use case instance with business logic.
        - **logout_type**: Logout type.

        ## Returns:
        - **JSONResponse**: Confirmation message indicating successful logout.

        ## Notes:
        - If `everywhere` is True, all user sessions are invalidated; otherwise, only
                the current session is logged out.
        """

        return JSONResponse(
            content=(
                await auth_usecase.delete_tokens(
                    token=token,
                    logout_type=logout_type,
                )
            ).model_dump(),
            status_code=status.HTTP_200_OK,
        )

    @staticmethod
    async def update_access_token(
        auth_usecase: Annotated[IAuthUC, Depends(get_auth_usecase)],
        body: RefreshToken,
        user_agent: Annotated[str | None, Header(alias="User-Agent")] = None,
    ) -> LoginToken:
        """
        Refresh the access token using the provided refresh token.

        ## Parameters:
        - **refreshToken**: The RefreshToken object containing the refresh token to be
                validated.

        ## Returns:
        - **LoginToken**: New access and refresh token pair.

        ## Notes:
        - This endpoint validates the refresh token, deletes the old session, and issues
                new tokens.
        """

        return await auth_usecase.update_access_token(
            refresh_token=body.refresh_token, user_agent=user_agent
        )

    @staticmethod
    async def register(
        user_in: UserCreate,
        auth_usecase: Annotated[IAuthUC, Depends(get_auth_usecase)],
        user_agent: Annotated[str | None, Header(alias="User-Agent")] = None,
    ) -> LoginToken:
        """
        Register a new user.

        ## Parameters:
        - **user_in**: UserCreate schema containing the data for the new user

        ## Returns:
        - **accessToken**: JWT access token for API authorization
        - **refreshToken**: JWT token for obtaining new access tokens

        ## Notes:
        - May trigger an error if a user with the same email already exists
        """

        return await auth_usecase.register(user_in=user_in, user_agent=user_agent)
