import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.client.storages.postgres.init.constants import PostgresInitEnums
from src.config.settings import Settings
from src.modules.users.interfaces import IRolePostgresRepo
from src.modules.users.schemas import RoleCreate


class PostgresInitializer:
    def __init__(
        self,
        db: AsyncSession,
        enums: PostgresInitEnums,
        settings: Settings,
        role_postgres_repo: IRolePostgresRepo,
    ):
        self._db = db
        self._enums = enums
        self._logger = logging.getLogger(__name__)
        self._settings = settings
        self._role_postgres_repo = role_postgres_repo

    async def _init_pg_vector(self):
        self._logger.info("Starting vector initialization")

        await self._db.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        await self._db.commit()

        self._logger.info("Completed vector initialization")

    async def _init_user_roles(self):
        self._logger.info("Starting user roles initialization")

        # TODO: add user roles initialization

        for id_, name in self._enums.User.Role.get_all_roles():
            role = await self._role_postgres_repo.get_by_id(id=id_)
            if role is not None:
                self._logger.info("User role %d already exist.", id_)
            else:
                await self._role_postgres_repo.create(
                    obj_in=RoleCreate(
                        id=id_,
                        name=name,
                    )
                )
                self._logger.info("User role created: %d", id_)

        self._logger.info("Completed user roles initialization")

    async def init(self) -> None:
        await self._init_pg_vector()
        await self._init_user_roles()
