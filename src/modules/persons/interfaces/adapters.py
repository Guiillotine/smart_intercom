from abc import ABC, abstractmethod

from sqlalchemy.sql.base import ExecutableOption

from src.common.interfaces import IPostgresBaseRepo
from src.common.schemas import Pagination, SortBase
from src.modules.persons.filters import PersonFilter
from src.modules.persons.models import PersonModel
from src.modules.persons.schemas import PersonCreate, PersonUpdate


class IPersonPostgresRepo(
    IPostgresBaseRepo[PersonModel, PersonCreate, PersonUpdate], ABC
):
    """
    Abstract interface for person-specific repository operations.

    Extends the generic IPostgresBaseRepo to include queries for managing shared
    person records in the PostgreSQL database.
    """

    @abstractmethod
    async def get_all_paginated(
        self,
        pagination_params: Pagination,
        filters: PersonFilter = None,
        sort_params: SortBase = None,
        custom_options: tuple[ExecutableOption, ...] = None,
    ) -> tuple[list[PersonModel], int]:
        """
        Retrieve a paginated list of persons.

        :param pagination_params: Pagination settings.
        :param filters: Optional FastApi SQLAlchemy model filters.
        :param sort_params: Optional sort params.
        :param custom_options: Optional SQLAlchemy loader options.
        :return: Tuple of person models and total count.
        """
        ...

    @abstractmethod
    async def create(
        self, obj_in: PersonCreate, with_commit: bool = True
    ) -> PersonModel:
        """
        Create a new person record in the database.

        :param obj_in: Input schema instance.
        :param with_commit: Whether to immediately commit the transaction.
        :return: The newly created person instance.
        """
