import logging
from typing import TYPE_CHECKING
from uuid import UUID

from src.common.constants import ErrorCodesEnums
from src.common.decorators import LoggingFunctionInfo
from src.common.errors import BackendException
from src.common.schemas import Msg, Pagination, PaginationResult, SortBase
from src.modules.persons.filters import PersonFilter
from src.modules.persons.interfaces import IPersonPostgresRepo, IPersonSrv
from src.modules.persons.schemas import PersonCreate, Person, PersonUpdate

if TYPE_CHECKING:
    from src.modules.persons.models import PersonModel


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

    @LoggingFunctionInfo(description="Get person by sid.")
    async def get_by_sid(self, sid: UUID) -> Person:
        return Person.model_validate(
            await self._person_postgres_repo.get_by_sid(sid)
        )

    @LoggingFunctionInfo(description="Search person by face embedding.")
    async def search_by_face_embedding(self, embedding: list[float]) -> UUID | None:
        # TODO: search by embedding
        pass

    @LoggingFunctionInfo(description="Create person.")
    async def create(self, person_in: PersonCreate) -> Person:
        return Person.model_validate(
            await self._person_postgres_repo.create(obj_in=person_in)
        )

    @LoggingFunctionInfo(description="Update person.")
    async def update(self, sid: UUID, person_in: PersonUpdate) -> Person:
        person = await self._get_model_by_sid(sid)

        return Person.model_validate(
            await self._person_postgres_repo.update(
                db_obj=person,
                obj_in=person_in,
            )
        )

    @LoggingFunctionInfo(description="Get person list.")
    async def get_all_paginated(
        self,
        pagination_params: Pagination,
        filters: PersonFilter = None,
        sort_params: SortBase = None,
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
    async def soft_delete(self, sid: UUID) -> Msg:
        person = await self._get_model_by_sid(sid)

        if not person:
            raise BackendException(error=self._errors.Person.PERSON_NOT_FOUND)

        await self._person_postgres_repo.update(
            db_obj=person,
            obj_in=PersonUpdate(is_archived=True),
        )

        return Msg()

    async def _get_model_by_sid(
        self,
        sid: UUID,
    ) -> "PersonModel":
        person = await self._person_postgres_repo.get_by_sid(sid)

        if not person:
            raise BackendException(self._errors.Person.PERSON_NOT_FOUND)

        return person
