import logging
from datetime import timedelta
from uuid import UUID, uuid4

from src.common.constants import ErrorCodesEnums
from src.common.decorators import LoggingFunctionInfo
from src.common.errors import BackendException
from src.common.interfaces import ITokenHelper
from src.config.settings import Settings
from src.modules.users.interfaces import ITokenProviderSrv, IAuthRedisRepo
from src.modules.users.schemas import LoginToken, AccessToken
from src.modules.users.services.constants.enums import AuthSrvEnums


class TokenProviderSrv(ITokenProviderSrv):
    """
    Service for handling token-related business logic.

    Responsibilities:
    - Generate token pairs using TokenHelper.
    - Decode and validate JWT tokens.
    """

    def __init__(
        self,
        enums: AuthSrvEnums,
        errors: ErrorCodesEnums,
        logger: logging.Logger,
        settings: Settings,
        token_helper: ITokenHelper,
        auth_redis_repository: IAuthRedisRepo,
    ):
        """
        Initialize TokenService.

        :param enums: Enums for all Auth services.
        :param logger: Logger instance for structured logging.
        :param settings: Settings for project.
        :param token_helper: Token helper instance that encapsulates token logic.
        :param auth_redis_repository: Repository for token persistence.
        """

        self._enums = enums
        self._errors = errors
        self._logger = logger
        self._settings = settings
        self._token_helper = token_helper
        self._auth_redis_repository = auth_redis_repository

    @LoggingFunctionInfo(
        description="Generate a pair of JWT tokens (access and refresh) with "
        "unique JTIs",
    )
    async def create_token_pair(self, payload: dict) -> LoginToken:
        self._logger.debug("Creating token pair for payload: %s", payload)

        pair_id, access_jti, refresh_jti = uuid4(), uuid4(), uuid4()

        access_token = self._token_helper.create_token(
            jti=access_jti,
            data=payload,
            pair_id=pair_id,
            expires_delta=timedelta(
                seconds=self._settings.project.ACCESS_TOKEN_EXPIRE_SECONDS,
            ),
            refresh=False,
        )
        refresh_token = self._token_helper.create_token(
            jti=refresh_jti,
            data=payload,
            pair_id=pair_id,
            expires_delta=timedelta(
                seconds=self._settings.project.REFRESH_TOKEN_EXPIRE_SECONDS,
            ),
            refresh=True,
        )

        await self._auth_redis_repository.set_with_ttl(
            key=f"{payload.get(self._enums.TokenEnums.AuthPayloadFields.SUB)}:"
            f"{pair_id}:"
            f"{access_jti}",
            ttl=self._settings.project.ACCESS_TOKEN_EXPIRE_SECONDS,
            value=access_token,
        )
        await self._auth_redis_repository.set_with_ttl(
            key=f"{payload.get(self._enums.TokenEnums.AuthPayloadFields.SUB)}:"
            f"{pair_id}:"
            f"{refresh_jti}",
            ttl=self._settings.project.REFRESH_TOKEN_EXPIRE_SECONDS,
            value=refresh_token,
        )

        self._logger.debug(
            "Token pair created. Access JTI: %s, Refresh JTI: %s",
            access_jti, refresh_jti,
        )

        return LoginToken(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    @LoggingFunctionInfo(description="Generate an access JWT token with unique JTIs")
    async def create_access_token(self, entity_sid: UUID, payload: dict) -> AccessToken:
        self._logger.debug("Creating token pair for payload: %s", payload)

        pair_id, access_jti = uuid4(), uuid4()

        access_token = self._token_helper.create_token(
            jti=access_jti,
            data=payload,
            pair_id=pair_id,
            expires_delta=timedelta(
                seconds=self._settings.project.ACCESS_TOKEN_EXPIRE_SECONDS,
            ),
            refresh=False,
        )

        key = self.prepare_token_key(entity_sid, pair_id, access_jti)
        await self._auth_redis_repository.set_with_ttl(
            key=key,
            ttl=self._settings.project.ACCESS_TOKEN_EXPIRE_SECONDS,
            value=access_token,
        )

        self._logger.debug("Token created. Access JTI: %s",access_jti)

        return AccessToken(access_token=access_token)

    @LoggingFunctionInfo(
        description="Decode and validate JWT token using project secret and algorithm"
    )
    async def validate_token(self, token: str) -> dict:
        """
        Decode a JWT token and return its payload.

        :param token: Encoded JWT token.
        :return: Decoded payload as dictionary.
        """
        return self._token_helper.decode_token(token=token)

    @LoggingFunctionInfo(description="Delete a token from Redis by its key")
    async def delete_token(self, key: str):
        await self._auth_redis_repository.delete(key=key)

    @LoggingFunctionInfo(
        description="Delete all user tokens matching the specified prefix in Redis"
    )
    async def delete_user_tokens(self, prefix: str):
        await self._auth_redis_repository.delete_by_prefix(prefix=prefix)

    @LoggingFunctionInfo(description="Get a token from Redis by its key")
    async def get_token_by_key(self, key: str) -> str:
        token = await self._auth_redis_repository.get(key=key)

        if not token:
            raise BackendException(self._errors.Token.TOKEN_NOT_FOUND)

        return token

    @staticmethod
    def prepare_token_key(entity_sid: UUID, pair_id: UUID, jti: UUID) -> str:
        return f"{entity_sid}:{pair_id}:{jti}"
