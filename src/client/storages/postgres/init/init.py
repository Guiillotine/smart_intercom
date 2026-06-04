import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.interfaces import IPasswordHelper
from src.client.storages.postgres.init.constants import PostgresInitEnums
from src.config.settings import Settings
from src.modules.users.interfaces import IRolePostgresRepo, IUserPostgresRepo
from src.modules.users.schemas import RoleCreate, UserCreateInDB


class PostgresInitializer:
    def __init__(
        self,
        db: AsyncSession,
        enums: PostgresInitEnums,
        settings: Settings,
        role_postgres_repo: IRolePostgresRepo,
        user_postgres_repo: IUserPostgresRepo,
        password_helper: IPasswordHelper,
    ):
        self._db = db
        self._enums = enums
        self._logger = logging.getLogger(__name__)
        self._settings = settings
        self._role_postgres_repo = role_postgres_repo
        self._user_postgres_repo = user_postgres_repo
        self._password_helper = password_helper

    async def _init_pg_vector(self):
        self._logger.info("Starting vector initialization")

        await self._db.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        await self._db.commit()

        self._logger.info("Completed vector initialization")

    async def _init_user_roles(self):
        self._logger.info("Starting user roles initialization")

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

    async def _init_superuser(self):
        self._logger.info("Starting superuser initialization")

        email = self._settings.auth.SUPERUSER_EMAIL
        existing_user = await self._user_postgres_repo.get_by_email(email=email)
        if existing_user is not None:
            self._logger.info("Superuser %s already exists.", email)
            return

        await self._user_postgres_repo.create(
            obj_in=UserCreateInDB(
                first_name=self._settings.auth.SUPERUSER_FIRST_NAME,
                last_name=self._settings.auth.SUPERUSER_LAST_NAME,
                email=email,
                password_hash=self._password_helper.get_password_hash(
                    self._settings.auth.SUPERUSER_PASSWORD,
                ),
                role_id=self._enums.User.Role.SUPERUSER,
            )
        )

        self._logger.info("Superuser %s created.", email)

    async def init(self) -> None:
        await self._init_pg_vector()
        await self._init_user_roles()
        await self._init_superuser()
