import hashlib
import logging
from uuid import UUID

from src.common.constants import ErrorCodesEnums
from src.common.errors import BackendException
from src.modules.users.interfaces import IUserPostgresRepo, IUserSrv
from src.modules.users.schemas import (
    UserCreate,
    UserCreateDB,
    UserWithPassword,
    UserWithRole,
)
from src.modules.users.services.constants import UserSrvConsts, UserSrvEnums


class UserSrv(IUserSrv):
    def __init__(
        self,
        errors: ErrorCodesEnums,
        enums: UserSrvEnums,
        consts: UserSrvConsts,
        logger: logging.Logger,
        user_repo: IUserPostgresRepo,
    ):
        self._errors = errors
        self._enums = enums
        self._consts = consts
        self._logger = logger
        self._user_repo = user_repo

    async def get_by_sid(self, sid: UUID) -> UserWithRole:
        user = await self._user_repo.get_by_sid(sid)
        if not user:
            raise BackendException(error=self._errors.Common.NOT_FOUND)
        return UserWithRole.model_validate(user)

    async def get_by_email(self, email: str) -> UserWithPassword | None:
        user = await self._user_repo.get_by_email(email)
        return UserWithPassword.model_validate(user) if user else None

    async def create(self, user_in: UserCreate) -> UserWithRole:
        user = await self._user_repo.create(
            obj_in=UserCreateDB(
                first_name=user_in.first_name,
                last_name=user_in.last_name,
                middle_name=user_in.middle_name,
                email=user_in.email,
                password_hash=self.hash_password(user_in.password),
            )
        )
        return UserWithRole.model_validate(user)

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()
