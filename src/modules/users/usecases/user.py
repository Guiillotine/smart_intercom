from uuid import UUID

from src.modules.users.interfaces import IUserSrv, IUserUC
from src.modules.users.schemas import UserWithRole
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
