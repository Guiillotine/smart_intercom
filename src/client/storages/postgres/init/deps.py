from sqlalchemy.ext.asyncio import AsyncSession

from src.client.storages.postgres.init import PostgresInitializer
from src.client.storages.postgres.init.constants.deps import get_postgres_init_enums
from src.common.constants.deps import get_common_enums, get_error_codes_enums
from src.common.logger.constants.deps import get_logger_config
from src.common.logger.deps import get_base_logger, get_logger_manager
from src.config.settings.deps import get_settings
from src.modules.users.adapters.repositories.postgres.deps import get_role_pg_repo
from src.modules.users.constants.deps import get_user_common_enums


async def get_postgres_initializer(db: AsyncSession) -> PostgresInitializer:
    logger = get_base_logger(get_logger_manager(get_logger_config()))
    error_codes = get_error_codes_enums()

    # Initialize role repository with database access and utilities
    role_postgres_repo = await get_role_pg_repo(
        db=db,
        logger=logger,
        error_codes=error_codes,
    )
    common_enums = get_common_enums()

    return PostgresInitializer(
        db=db,
        enums=await get_postgres_init_enums(
            user_common_enums=get_user_common_enums(
                common_enums=common_enums,
            ),
        ),
        settings=get_settings(),
        role_postgres_repo=role_postgres_repo,
    )
