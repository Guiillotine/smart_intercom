import logging

from fastapi.security import OAuth2PasswordRequestForm
from src.common.constants import ErrorCodesEnums
from src.common.decorators import LoggingFunctionInfo
from src.common.errors import BackendException
from src.common.interfaces import IPasswordHelper
from src.config.settings import Settings
from src.modules.users.interfaces import IAuthSrv, IAuthRedisRepo, IUserSrv
from src.modules.users.schemas import User
from src.modules.users.services.constants.enums import AuthSrvEnums


class AuthSrv(IAuthSrv):
    """
    Service responsible for user authentication and credential management.

    Implements IAuthManagerSrv interface to provide:
    - User authentication via email/password
    - Credential validation
    - Integration with IAM system
    """

    def __init__(
        self,
        enums: AuthSrvEnums,
        errors: ErrorCodesEnums,
        logger: logging.Logger,
        settings: Settings,
        password_helper: IPasswordHelper,
        user_service: IUserSrv,
        auth_redis_repository: IAuthRedisRepo,
    ):
        self._enums = enums
        self._errors = errors
        self._logger = logger
        self._settings = settings
        self._password_helper = password_helper
        self._user_service = user_service
        self._auth_redis_repository = auth_redis_repository

    @LoggingFunctionInfo(
        description="Authenticates a user using the provided credentials "
        "(email and password).",
    )
    async def authenticate(
        self,
        credentials: OAuth2PasswordRequestForm,
    ) -> User:
        await self._auth_redis_repository.get(
            key=f"login_counter:{credentials.username}"
        )

        self._logger.debug("Authenticating user: %s", credentials.username)

        user = await self._user_service.get_by_email(email=credentials.username)

        if not user:
            raise BackendException(self._errors.Auth.INCORRECT_CREDENTIALS)

        if not self._password_helper.verify_password(
            credentials.password,
            user.password_hash,
        ):
            raise BackendException(self._errors.Auth.INCORRECT_CREDENTIALS)

        self._logger.debug("User authenticated successfully: %s", user.email)
        return user
