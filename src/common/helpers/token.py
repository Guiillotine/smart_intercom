import logging
from datetime import timedelta
from uuid import UUID

from jose import jwt

from src.common.constants import TokenEnums
from src.common.interfaces import ITokenHelper, ICustomDateTime
from src.config.settings import Settings


class TokenHelper(ITokenHelper):
    """
    A helper class for handling JWT token creation, decoding, and validation.

    Responsibilities:
    - Generate access and refresh tokens with expiration and unique JTI.
    - Decode and validate JWT payloads based on token type (access/refresh).
    - Store token JTIs in Redis for blacklisting or tracking.
    """

    def __init__(
        self,
        enums: TokenEnums,
        logger: logging.Logger,
        settings: Settings,
        custom_datetime: ICustomDateTime,
    ):
        """
        Initializes the TokenHelper instance.

        :param enums: AuthHlpEnums instance containing necessary enums for token
                handling.
        :param logger: Logger for recording token operations and errors.
        :param settings: Application settings containing token configuration
                (e.g., secret keys, expiration times).
        :param custom_datetime: Custom datetime provider for handling token expiration
                and issuance times.
        """

        self._enums = enums
        self._logger = logger
        self._settings = settings
        self._custom_datetime = custom_datetime

    def create_token(
        self,
        jti: UUID,
        data: dict,
        pair_id: UUID,
        expires_delta: timedelta,
        refresh: bool = False,
    ) -> str:
        self._logger.debug("Creating token. Refresh: %s, JTI: %s", refresh, jti)
        to_encode = data.copy()

        expire = self._custom_datetime.get_datetime_w_timezone() + expires_delta
        to_encode.update(
            {
                self._enums.AuthPayloadFields.EXP: expire,
                self._enums.AuthPayloadFields.JTI: str(jti),
                self._enums.AuthPayloadFields.PAIR_ID: str(pair_id),
            },
        )

        token_type = (
            self._enums.TokenType.REFRESH if refresh else self._enums.TokenType.ACCESS
        )
        to_encode.update({"token": token_type})

        encoded_jwt = jwt.encode(
            to_encode,
            self._settings.auth.TOKEN_SECRET_KEY,
            algorithm=self._settings.auth.ALGORITHM,
        )

        self._logger.debug("Token created successfully. Payload: %s", to_encode)

        return encoded_jwt

    def decode_token(self, token: str) -> dict:
        self._logger.debug("Decoding token")
        return jwt.get_unverified_claims(token)
