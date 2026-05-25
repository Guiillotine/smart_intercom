import logging
from typing import Annotated

from fastapi import Depends

from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes_enums
from src.common.helpers.deps import get_password_helper, get_token_helper
from src.common.interfaces import IPasswordHelper, ITokenHelper
from src.common.logger.deps import get_user_logger
from src.config.settings import Settings
from src.config.settings.deps import get_settings
from src.modules.users.adapters.repositories.postgres.deps import get_user_pg_repo
from src.modules.users.adapters.repositories.redis.deps import get_auth_redis_repository
from src.modules.users.interfaces import IUserPostgresRepo, IUserSrv, IAuthSrv, \
    IAuthRedisRepo, ITokenProviderSrv
from src.modules.users.services.auth import AuthSrv
from src.modules.users.services.constants import UserSrvConsts, UserSrvEnums
from src.modules.users.services.constants.deps import (
    get_user_srv_consts,
    get_user_srv_enums, get_auth_srv_enums,
)
from src.modules.users.services.constants.enums import AuthSrvEnums
from src.modules.users.services.token import TokenProviderSrv
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

async def get_auth_service(
    enums: Annotated[AuthSrvEnums, Depends(get_auth_srv_enums)],
    logger: Annotated[logging.Logger, Depends(get_user_logger)],
    settings: Annotated[Settings, Depends(get_settings)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
    password_helper: Annotated[IPasswordHelper, Depends(get_password_helper)],
    user_service: Annotated[IUserSrv, Depends(get_user_service)],
    auth_redis_repository: Annotated[
        IAuthRedisRepo, Depends(get_auth_redis_repository),
    ],
) -> IAuthSrv:
    return AuthSrv(
        enums=enums,
        errors=error_codes,
        logger=logger,
        settings=settings,
        password_helper=password_helper,
        user_service=user_service,
        auth_redis_repository=auth_redis_repository,
    )


async def get_token_provider_service(
    enums: Annotated[AuthSrvEnums, Depends(get_auth_srv_enums)],
    logger: Annotated[logging.Logger, Depends(get_user_logger)],
    settings: Annotated[Settings, Depends(get_settings)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
    token_helper: Annotated[ITokenHelper, Depends(get_token_helper)],
    auth_redis_repository: Annotated[
        IAuthRedisRepo,
        Depends(get_auth_redis_repository),
    ],
) -> ITokenProviderSrv:
    return TokenProviderSrv(
        enums=enums,
        errors=error_codes,
        logger=logger,
        settings=settings,
        token_helper=token_helper,
        auth_redis_repository=auth_redis_repository,
    )
