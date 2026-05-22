import logging
from uuid import UUID

from fastapi.security import OAuth2PasswordRequestForm

from src.common.constants import ErrorCodesEnums
from src.common.decorators import LoggingFunctionInfo
from src.common.errors import BackendException
from src.common.schemas import Msg
from src.config.settings import Settings
from src.modules.users.constants.enums import RoleEnum, LogoutType
from src.modules.users.interfaces import IAuthUC, IUserSrv
from src.modules.users.schemas import LoginToken, UserCreate
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
        user_service: IUserSrv,
    ):
        self._logger = logger
        self._errors = errors
        self._enums = enums
        self._consts = consts
        self._settings = settings
        self._user_service = user_service

    async def _create_token_payload(
        self, user_sid: UUID, role: RoleEnum
    ) -> dict:
        self._logger.debug(
            "Preparing payload for the token: user_sid=%s, role=%s",
            user_sid,
            role,
        )

        return {
            self._enums.Token.AuthPayloadFields.SUB: str(user_sid),
            self._enums.Token.AuthPayloadFields.STATUS: role,
        }

    @LoggingFunctionInfo(
        description="Generate a pair of access and refresh tokens for the user.",
    )
    async def get_token_pair(
        self,
        form_data: OAuth2PasswordRequestForm,
        user_agent: str,
    ) -> LoginToken:
        self._logger.debug("Authenticate the user")
        user = await self._auth_manager_service.authenticate(form_data)

        payload = await self._create_token_payload(
            user_sid=user.sid,
            role=user.role,
        )

        self._logger.debug("Generating token pair for user %s.", user.sid)
        return await self._token_provider_service.create_token_pair(payload=payload)

    @LoggingFunctionInfo(
        description="Validate refresh token, delete old session, and generate new "
        "access token pair",
    )
    async def update_access_token(
        self,
        refresh_token: str,
        user_agent: str,
    ) -> LoginToken:
        try:
            self._logger.debug("Validate the refresh token")
            payload = await self._token_provider_service.validate_token(refresh_token)

            self._logger.debug("Validate existing refresh token")
            await self._token_provider_service.get_token_by_key(
                key=f"{payload[self._enums.Token.AuthPayloadFields.SUB]}:"
                f"{payload[self._enums.Token.TokenPayloadFields.PAIR_ID]}:"
                f"{payload[self._enums.Token.TokenPayloadFields.JTI]}"
            )
        except Exception as e:
            self._logger.error("Failed to validate refresh token: %s", e)
            raise BackendException(self._errors.Token.INVALID_REFRESH_TOKEN) from e

        self._logger.debug("Delete the old session")
        await self._token_provider_service.delete_user_tokens(
            prefix=f"{payload[self._enums.Token.AuthPayloadFields.SUB]}:"
            f"{payload[self._enums.Token.TokenPayloadFields.PAIR_ID]}",
        )

        self._logger.debug(
            "Refreshing access token for user %s",
            payload[self._enums.Token.AuthPayloadFields.SUB],
        )

        new_payload = await self._create_token_payload(
            user_sid=payload.get(self._enums.Token.AuthPayloadFields.SUB),
            statuses=payload.get(self._enums.Token.AuthPayloadFields.STATUS),
        )

        return await self._token_provider_service.create_token_pair(payload=new_payload)

    @LoggingFunctionInfo(
        description="Validate token and delete user tokens either for current session "
        "or all sessions",
    )
    async def delete_tokens(
        self,
        token: str,
        logout_type: LogoutType,
    ) -> Msg:
        try:
            self._logger.debug("Validating token for deletion")
            payload = await self._token_provider_service.validate_token(token)
        except BackendException as e:
            self._logger.error("Failed to validate refresh token: %s", e)
            raise BackendException(self._errors.Token.INVALID_ACCESS_TOKEN) from e

        if logout_type == self._enums.Auth.LogoutType.everywhere:
            self._logger.debug(
                "Deleting all tokens for user %s",
                payload[self._enums.Token.AuthPayloadFields.SUB],
            )
            await self._token_provider_service.delete_user_tokens(
                prefix=f"{payload[self._enums.Token.AuthPayloadFields.SUB]}",
            )
        elif logout_type == self._enums.Auth.LogoutType.current:
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
        elif logout_type == self._enums.Auth.LogoutType.other:
            pair_id = payload[self._enums.Token.TokenPayloadFields.PAIR_ID]
            user_sid = payload[self._enums.Token.AuthPayloadFields.SUB]

            self._logger.debug(
                "Deleting token for user %s exclude session %s",
                user_sid,
                pair_id,
            )
            await self._token_provider_service.delete_all_user_sessions_except(
                user_sid=user_sid,
                pair_id=pair_id,
            )

        self._logger.info(
            "Tokens deleted successfully for user %s",
            payload[self._enums.Token.AuthPayloadFields.SUB],
        )

        return Msg()

    @LoggingFunctionInfo(
        description="Register a new user after verifying email status.",
    )
    async def register(self, user_in: UserCreate, user_agent: str) -> LoginToken:
        self._logger.debug("Creating new user with email: %s", user_in.email)

        user = await self._user_service.create(user_in=user_in)

        payload = await self._create_token_payload(
            user_sid=user.sid,
            role=user.role,
        )

        self._logger.debug("Generating token pair for user %s.", user.sid)

        return await self._token_provider_service.create_token_pair(payload=payload)
