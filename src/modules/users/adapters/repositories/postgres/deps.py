import logging
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from src.client.storages.deps import get_db
from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes_enums
from src.common.logger.deps import get_user_logger
from src.modules.users.adapters.repositories.postgres import RolePostgresRepo
from src.modules.users.interfaces import IRolePostgresRepo


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
