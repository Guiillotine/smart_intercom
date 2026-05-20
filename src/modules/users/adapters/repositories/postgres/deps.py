import logging
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.client.storages.deps import get_db
from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes_enums
from src.common.logger.deps import get_user_logger
from src.modules.users.adapters.repositories.postgres.constants import (
    UserRepoConsts,
    UserRepoEnums,
)
from src.modules.users.adapters.repositories.postgres.constants.deps import (
    get_user_repo_consts,
    get_user_repo_enums,
)
from src.modules.users.adapters.repositories.postgres import RolePostgresRepo, UserPostgresRepo
from src.modules.users.interfaces import IRolePostgresRepo, IUserPostgresRepo


async def get_role_pg_repo(
    db: Annotated[AsyncSession, Depends(get_db)],
    logger: Annotated[logging.Logger, Depends(get_user_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
) -> IRolePostgresRepo:
    """Dependency provider for RolePostgresRepo instance.

    :param db: Async database session dependency
    :param logger: Configured logger instance dependency
    :param error_codes: Error codes enum dependency

    :return: Initialized role repository instance
    """
    return RolePostgresRepo(db=db, errors=error_codes, logger=logger)


async def get_user_pg_repo(
    db: Annotated[AsyncSession, Depends(get_db)],
    logger: Annotated[logging.Logger, Depends(get_user_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
    enums: Annotated[UserRepoEnums, Depends(get_user_repo_enums)],
    consts: Annotated[UserRepoConsts, Depends(get_user_repo_consts)],
) -> IUserPostgresRepo:
    return UserPostgresRepo(
        db=db,
        errors=error_codes,
        logger=logger,
        enums=enums,
        consts=consts,
    )
