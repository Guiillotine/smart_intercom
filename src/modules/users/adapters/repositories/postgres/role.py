import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.common.adapters.repositories.postgres import PostgresBaseRepo
from src.common.constants import ErrorCodesEnums
from src.modules.users.interfaces import IRolePostgresRepo
from src.modules.users.models import RoleModel
from src.modules.users.schemas import RoleCreate, RoleUpdate


class RolePostgresRepo(
    PostgresBaseRepo[RoleModel, RoleCreate, RoleUpdate], IRolePostgresRepo,
):
    """
    Repository for managing user role data in PostgreSQL database.

    Provides specialized operations for role management, extending basic CRUD
    functionality from PostgresBaseRepo and implementing IRolePostgresRepo interface.
    """

    def __init__(
        self,
        db: AsyncSession,
        errors: ErrorCodesEnums,
        logger: logging.Logger,
    ):
        """Initialize the member type repository instance.

        :param db: Async scoped session for database operations
        :param errors: Enum containing all error codes for member type operations
        :param logger: Configured logger instance for repository logging
        """
        super().__init__(db=db, model=RoleModel, errors=errors, logger=logger)
        self._errors = errors
        self._logger = logger
