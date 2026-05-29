import logging
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from src.common.adapters.repositories.postgres import PostgresBaseRepo
from src.common.constants import ErrorCodesEnums
from src.common.decorators import LoggingFunctionInfo
from src.common.schemas import Pagination, SortBase
from src.modules.persons.constants.enums import PersonTypeEnum
from src.modules.persons.filters import PersonFilter
from src.modules.persons.interfaces import IPersonPostgresRepo
from src.modules.persons.models import PersonModel
from src.modules.persons.schemas import PersonCreate, PersonUpdate


class PersonPostgresRepo(
    PostgresBaseRepo[PersonModel, PersonCreate, PersonUpdate],
    IPersonPostgresRepo,
):
    def __init__(
        self,
        db: AsyncSession,
        logger: logging.Logger,
        errors: ErrorCodesEnums,
        person_type: PersonTypeEnum | None = None,
    ):
        super().__init__(db=db, model=PersonModel, logger=logger, errors=errors)
        self._person_type = person_type

    @LoggingFunctionInfo(description="Retrieve a paginated list of persons.")
    async def get_all_paginated(
        self,
        pagination_params: Pagination,
        filters: PersonFilter = None,
        sort_params: SortBase = None,
        custom_options: tuple[ExecutableOption, ...] = None,
    ) -> tuple[list[PersonModel], int]:
        if self._person_type is not None:
            filters = filters or PersonFilter()
            filters.person_type = self._person_type

        return await super().get_all_paginated(
            pagination_params=pagination_params,
            filters=filters,
            sort_params=sort_params,
            custom_options=custom_options,
        )

    @LoggingFunctionInfo(
        description="Create a new content partition in the collection."
    )
    async def create(
        self,
        obj_in: PersonCreate,
    ) -> PersonModel:
        err_msg = "Person type is not set"

        person_type = (
            self._person_type
            if self._person_type is not None
            else obj_in.person_type
        )

        if person_type is None:
            raise ValueError(err_msg)

        obj_in.person_type = person_type

        return await super().create(obj_in=obj_in)

    @LoggingFunctionInfo(description="Search nearest person by face embedding.")
    async def search_by_face_embedding(
        self,
        embedding: list[float],
        max_distance: float,
    ) -> UUID | None:
        distance = PersonModel.face_embedding.cosine_distance(embedding).label(
            "distance"
        )
        query = (
            select(PersonModel.sid, distance)
            .where(PersonModel.is_archived.is_(False))
            .order_by(distance)
            .limit(1)
        )

        if self._person_type is not None:
            query = query.where(PersonModel.person_type == self._person_type)

        result = await self._db.execute(query)
        row = result.first()

        if row is None or row.distance is None or row.distance > max_distance:
            return None

        return row.sid
