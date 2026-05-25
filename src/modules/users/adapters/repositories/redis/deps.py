import logging
from typing import Annotated

from fastapi import Depends

from redis import Redis
from src.client.storages.deps import get_redis_client
from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes_enums
from src.common.logger.deps import get_user_logger
from src.modules.users.adapters.repositories.redis import AuthRedisRepo
from src.modules.users.interfaces import IAuthRedisRepo


async def get_auth_redis_repository(
    redis: Annotated[Redis, Depends(get_redis_client)],
    logger: Annotated[logging.Logger, Depends(get_user_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
) -> IAuthRedisRepo:
    return AuthRedisRepo(
        redis=redis,
        errors=error_codes,
        logger=logger,
    )
