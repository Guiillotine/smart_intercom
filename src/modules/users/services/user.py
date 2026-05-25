import logging
from uuid import UUID

from src.common.constants import ErrorCodesEnums
from src.common.errors import BackendException
from src.modules.users.interfaces import IUserPostgresRepo, IUserSrv
from src.modules.users.schemas import (
    UserWithPassword,
    UserWithRole,
    UserCreateInDB,
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

    async def create(self, user_in: UserCreateInDB) -> UserWithRole:
        user = await self._user_repo.create(obj_in=user_in)

        return UserWithRole.model_validate(user)
