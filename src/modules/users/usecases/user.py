import hashlib
from datetime import datetime, timedelta
from uuid import UUID, uuid4

from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from src.common.constants import ErrorCodesEnums, TokenEnums
from src.common.errors import BackendException
from src.common.schemas import Msg
from src.config.settings import Settings
from src.modules.users.constants.enums import LogoutType
from src.modules.users.interfaces import IAuthUC, IUserSrv, IUserUC
from src.modules.users.schemas import LoginToken, UserCreate, UserWithRole
from src.modules.users.usecases.constants import UserUCConsts, UserUCEnums


class UserUC(IUserUC):
    def __init__(
        self,
        enums: UserUCEnums,
        consts: UserUCConsts,
        user_service: IUserSrv,
    ):
        self._enums = enums
        self._consts = consts
        self._user_service = user_service

    async def get_user_info(self, user_sid: UUID) -> UserWithRole:
        return await self._user_service.get_by_sid(user_sid)

    async def get_by_sid(self, sid: UUID, user_sid: UUID) -> UserWithRole:
        return await self._user_service.get_by_sid(sid)


class AuthUC(IAuthUC):
    def __init__(
        self,
        errors: ErrorCodesEnums,
        token_enums: TokenEnums,
        enums: UserUCEnums,
        consts: UserUCConsts,
        settings: Settings,
        user_service: IUserSrv,
    ):
        self._errors = errors
        self._token_enums = token_enums
        self._enums = enums
        self._consts = consts
        self._settings = settings
        self._user_service = user_service

    async def get_token_pair(
        self, form_data: OAuth2PasswordRequestForm, user_agent: str | None = None
    ) -> LoginToken:
        user = await self._user_service.get_by_email(form_data.username)
        if not user or user.password_hash != self._hash_password(form_data.password):
            raise BackendException(error=self._errors.Auth.INCORRECT_CREDENTIALS)
        return self._create_token_pair(user.sid)

    async def register(
        self, user_in: UserCreate, user_agent: str | None = None
    ) -> LoginToken:
        user = await self._user_service.create(user_in)
        return self._create_token_pair(user.sid)

    async def update_access_token(
        self, refresh_token: str, user_agent: str | None = None
    ) -> LoginToken:
        payload = jwt.get_unverified_claims(refresh_token)
        return self._create_token_pair(UUID(payload[self._token_enums.AuthPayloadFields.SUB]))

    async def delete_tokens(self, token: str, logout_type: LogoutType) -> Msg:
        return Msg()

    def _create_token_pair(self, user_sid: UUID) -> LoginToken:
        payload = {
            self._token_enums.AuthPayloadFields.SUB: str(user_sid),
            self._token_enums.AuthPayloadFields.JTI: str(uuid4()),
            self._token_enums.AuthPayloadFields.PAIR_ID: str(uuid4()),
            self._token_enums.AuthPayloadFields.EXP: datetime.utcnow()
            + timedelta(days=1),
        }
        access_token = jwt.encode(
            {**payload, "token": self._token_enums.TokenType.ACCESS},
            self._settings.token.TOKEN_SECRET_KEY,
            algorithm=self._settings.token.ALGORITHM,
        )
        refresh_token = jwt.encode(
            {
                **payload,
                self._token_enums.AuthPayloadFields.EXP: datetime.utcnow()
                + timedelta(days=30),
                "token": self._token_enums.TokenType.REFRESH,
            },
            self._settings.token.TOKEN_SECRET_KEY,
            algorithm=self._settings.token.ALGORITHM,
        )
        return LoginToken(access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()
