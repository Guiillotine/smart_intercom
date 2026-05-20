import logging
from typing import Annotated

from fastapi import Depends

from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes_enums
from src.common.logger.deps import get_user_logger
from src.modules.users.adapters.repositories.postgres.deps import get_user_pg_repo
from src.modules.users.interfaces import IUserPostgresRepo, IUserSrv
from src.modules.users.services.constants import UserSrvConsts, UserSrvEnums
from src.modules.users.services.constants.deps import (
    get_user_srv_consts,
    get_user_srv_enums,
)
from src.modules.users.services.user import UserSrv


async def get_user_service(
    logger: Annotated[logging.Logger, Depends(get_user_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
    enums: Annotated[UserSrvEnums, Depends(get_user_srv_enums)],
    consts: Annotated[UserSrvConsts, Depends(get_user_srv_consts)],
    user_repo: Annotated[IUserPostgresRepo, Depends(get_user_pg_repo)],
) -> IUserSrv:
    return UserSrv(
        errors=error_codes,
        enums=enums,
        consts=consts,
        logger=logger,
        user_repo=user_repo,
    )
