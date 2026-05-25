import logging

from redis import Redis
from src.common.adapters.repositories.redis import BaseRedisRepo
from src.common.constants import ErrorCodesEnums
from src.modules.users.interfaces import IAuthRedisRepo


class AuthRedisRepo(BaseRedisRepo, IAuthRedisRepo):
    """
    Redis repository implementation for authentication-specific operations.

    Extends BaseRedisRepo with auth-specific functionality while implementing
    IAuthRedisRepo interface. Handles all Redis operations related to:
    - User sessions
    - Token management
    - Authentication state
    """

    def __init__(
        self,
        redis: Redis,
        errors: ErrorCodesEnums,
        logger: logging.Logger,
    ):
        """
        Initialize authentication Redis repository.

        :param redis: Configured Redis client instance for auth operations
        :param errors: Error codes enumeration for auth-specific exceptions
        :param logger: Configured logger instance for auth operations
        """

        super().__init__(
            redis=redis,
            errors=errors,
            logger=logger,
        )
