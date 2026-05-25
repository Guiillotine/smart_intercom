import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.adapters.repositories.postgres import PostgresBaseRepo
from src.common.constants import ErrorCodesEnums
from src.modules.users.interfaces import IUserPostgresRepo
from src.modules.users.models import UserModel
from src.modules.users.schemas import UserCreate, UserUpdate, UserCreateInDB
from src.modules.users.adapters.repositories.postgres.constants import (
    UserRepoConsts,
    UserRepoEnums,
)


class UserPostgresRepo(
    PostgresBaseRepo[UserModel, UserCreateInDB, UserUpdate], IUserPostgresRepo
):
    def __init__(
        self,
        db: AsyncSession,
        errors: ErrorCodesEnums,
        logger: logging.Logger,
        enums: UserRepoEnums,
        consts: UserRepoConsts,
    ):
        super().__init__(db=db, model=UserModel, errors=errors, logger=logger)
        self._enums = enums
        self._consts = consts

    async def get_by_email(self, email: str) -> UserModel | None:
        return await self._get_single_result(
            select(UserModel).where(UserModel.email == email)
        )
