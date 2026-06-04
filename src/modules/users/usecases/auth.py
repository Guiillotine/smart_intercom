import logging
from uuid import UUID

from fastapi.security import OAuth2PasswordRequestForm

from src.common.constants import ErrorCodesEnums
from src.common.decorators import LoggingFunctionInfo
from src.common.errors import BackendException
from src.common.interfaces import IPasswordHelper
from src.common.schemas import Msg
from src.config.settings import Settings
from src.modules.users.constants.enums import RoleEnum
from src.modules.users.interfaces import IAuthUC, IUserSrv, IAuthSrv, ITokenProviderSrv
from src.modules.users.schemas import (
    LoginToken,
    UserCreate,
    UserCreateByAdmin,
    UserCreateInDB,
    UserWithRole,
)
from src.modules.users.usecases.constants import AuthUCEnums
from src.modules.users.usecases.constants.consts import AuthUCConsts


class AuthUC(IAuthUC):
    def __init__(
        self,
        logger: logging.Logger,
        errors: ErrorCodesEnums,
        enums: AuthUCEnums,
        consts: AuthUCConsts,
        settings: Settings,
        password_helper: IPasswordHelper,
        user_service: IUserSrv,
        auth_service: IAuthSrv,
        token_provider_service: ITokenProviderSrv,
    ):
        self._logger = logger
        self._errors = errors
        self._enums = enums
        self._consts = consts
        self._settings = settings
        self._password_helper = password_helper
        self._user_service = user_service
        self._auth_service = auth_service
        self._token_provider_service = token_provider_service

    async def _create_token_payload(
        self, user_sid: UUID, role: RoleEnum
    ) -> dict:
        return {
            self._enums.Token.AuthPayloadFields.SUB: str(user_sid),
            self._enums.Token.AuthPayloadFields.STATUS: role,
        }

    @LoggingFunctionInfo(
        description="Generate a pair of access and refresh tokens for the user."
    )
    async def get_token_pair(
        self,
        form_data: OAuth2PasswordRequestForm,
    ) -> LoginToken:
        user = await self._auth_service.authenticate(form_data)

        payload = await self._create_token_payload(
            user_sid=user.sid,
            role=self._enums.User.Role(user.role_id),
        )

        return await self._token_provider_service.create_token_pair(payload=payload)

    @LoggingFunctionInfo(
        description="Validate refresh token, delete old session, and generate new "
        "access token pair"
    )
    async def update_access_token(
        self,
        refresh_token: str,
    ) -> LoginToken:
        try:
            payload = await self._token_provider_service.validate_token(refresh_token)

            await self._token_provider_service.get_token_by_key(
                key=f"{payload[self._enums.Token.AuthPayloadFields.SUB]}:"
                f"{payload[self._enums.Token.TokenPayloadFields.PAIR_ID]}:"
                f"{payload[self._enums.Token.TokenPayloadFields.JTI]}"
            )
        except Exception as e:
            raise BackendException(self._errors.Token.INVALID_REFRESH_TOKEN) from e

        self._logger.debug("Delete the old session")
        await self._token_provider_service.delete_user_tokens(
            prefix=f"{payload[self._enums.Token.AuthPayloadFields.SUB]}:"
            f"{payload[self._enums.Token.TokenPayloadFields.PAIR_ID]}",
        )

        new_payload = await self._create_token_payload(
            user_sid=payload.get(self._enums.Token.AuthPayloadFields.SUB),
            role=payload.get(self._enums.Token.AuthPayloadFields.STATUS),
        )

        return await self._token_provider_service.create_token_pair(payload=new_payload)

    @LoggingFunctionInfo(
        description="Validate token and delete user tokens either for current session "
        "or all sessions"
    )
    async def delete_token(
        self,
        token: str,
    ) -> Msg:
        try:
            payload = await self._token_provider_service.validate_token(token)
        except BackendException as e:
            raise BackendException(self._errors.Token.INVALID_ACCESS_TOKEN) from e

        pair_id = payload[self._enums.Token.TokenPayloadFields.PAIR_ID]
        user_sid = payload[self._enums.Token.AuthPayloadFields.SUB]

        self._logger.debug(
            "Deleting token for user %s session %s",
            user_sid,
            pair_id,
        )
        await self._token_provider_service.delete_user_tokens(
            prefix=f"{user_sid}:{pair_id}",
        )

        return Msg()

    @LoggingFunctionInfo(
        description="Register a new user after verifying email status."
    )
    async def register(self, user_in: UserCreate) -> LoginToken:
        self._logger.debug("Creating new user with email: %s", user_in.email)

        user = await self._user_service.create(
            user_in=UserCreateInDB(
                **user_in.model_dump(exclude={"password"}),
                password_hash=self._password_helper.get_password_hash(user_in.password),
                role_id=RoleEnum.USER,
            )
        )

        payload = await self._create_token_payload(
            user_sid=user.sid,
            role=self._enums.User.Role(user.role_id),
        )

        return await self._token_provider_service.create_token_pair(payload=payload)

    @LoggingFunctionInfo(
        description="Register a new user with selected role by administrator."
    )
    async def register_by_admin(
        self,
        user_in: UserCreateByAdmin,
        admin_user_sid: UUID,
    ) -> UserWithRole:
        admin_user = await self._user_service.get_by_sid(admin_user_sid)
        admin_role = RoleEnum(admin_user.role_id)

        if admin_role not in RoleEnum.get_admin_roles():
            raise BackendException(self._errors.Common.FORBIDDEN)

        if user_in.role_id == RoleEnum.SUPERUSER:
            raise BackendException(self._errors.Auth.INCORRECT_USER_ROLE)

        return await self._user_service.create(
            user_in=UserCreateInDB(
                **user_in.model_dump(exclude={"password"}),
                password_hash=self._password_helper.get_password_hash(user_in.password),
            )
        )
