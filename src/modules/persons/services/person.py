import logging
from uuid import UUID

from src.common.constants import ErrorCodesEnums
from src.common.decorators import LoggingFunctionInfo
from src.common.errors import BackendException
from src.common.schemas import Msg, Pagination, PaginationResult
from src.modules.persons.interfaces import IPersonPostgresRepo, IPersonSrv
from src.modules.persons.schemas import PersonCreate, Person, PersonUpdate, \
    PersonCreate


class PersonSrv(IPersonSrv):
    """
    Service layer for managing shared person records.

    Provides business logic operations related to persons and delegates database
    interactions to the person repository.
    """

    def __init__(
        self,
        errors: ErrorCodesEnums,
        logger: logging.Logger,
        person_postgres_repo: IPersonPostgresRepo,
    ):
        """
        Initialize the person service with dependencies.

        :param errors: ErrorCodesEnums instance for standardized error handling.
        :param logger: Configured logger instance.
        :param person_postgres_repo: Person repository.
        """

        self._errors = errors
        self._logger = logger
        self._person_postgres_repo = person_postgres_repo

    @LoggingFunctionInfo(description="Create person.")
    async def create(self, person_in: PersonCreate) -> Person:
        return Person.model_validate(
            await self._person_postgres_repo.create(obj_in=person_in)
        )

    @LoggingFunctionInfo(description="Update person.")
    async def update(self, sid: UUID, person_in: PersonUpdate) -> Person:
        person = await self._person_postgres_repo.get_by_sid(sid=sid)
        if not person:
            raise BackendException(error=self._errors.Common.ENTITY_NOT_FOUND)

        return Person.model_validate(
            await self._person_postgres_repo.update(
                db_obj=person,
                obj_in=person_in,
            )
        )

    @LoggingFunctionInfo(description="Get person list.")
    async def get_all(
        self,
        pagination_params: Pagination,
        person_type: int | None = None,
    ) -> PaginationResult[Person]:
        persons, total = await self._person_postgres_repo.get_all_paginated(
            pagination_params=pagination_params,
        )
        return PaginationResult(
            items=[Person.model_validate(person) for person in persons],
            limit=pagination_params.limit,
            offset=pagination_params.offset,
            total=total,
        )

    @LoggingFunctionInfo(description="Delete person.")
    async def delete(self, sid: UUID) -> Msg:
        person = await self._person_postgres_repo.delete(sid=sid)
        if not person:
            raise BackendException(error=self._errors.Common.ENTITY_NOT_FOUND)

        return Msg()
