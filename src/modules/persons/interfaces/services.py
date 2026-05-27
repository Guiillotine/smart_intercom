from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from src.common.schemas import Msg, Pagination, PaginationResult, SortBase
from src.modules.persons.filters import PersonFilter
from src.modules.persons.schemas import PersonCreate, PersonUpdate, Person


class IPersonSrv(ABC):
    """
    Interface for shared person service operations.
    """

    @abstractmethod
    async def get_all_paginated(
        self,
        pagination_params: Pagination,
        filters: PersonFilter = None,
        sort_params: SortBase = None,
    ) -> PaginationResult[Person]:
        """
        Retrieve a paginated list of persons.

        :param pagination_params: Pagination settings.
        :param filters: Optional FastApi SQLAlchemy filters.
        :param sort_params: Optional sort params.
        :return: Paginated list of persons.
        """
        ...

    @abstractmethod
    async def get_by_sid(self, sid: UUID) -> Person:
        """
        Retrieve a person by sid.

        :param sid: Person identifier.
        :return: Person data.
        """
        ...

    @abstractmethod
    async def search_by_face_embedding(self, embedding: list[float]) -> UUID | None:
        """
        Search person by face embedding.

        :param embedding: Face embedding.
        :return: Identifier of found person or None if not found.
        """
        ...

    @abstractmethod
    async def create(self, person_in: PersonCreate) -> Person:
        """
        Create a person record.

        :param person_in: Person data for creation.
        :return: Created person data.
        """
        ...

    @abstractmethod
    async def update(self, sid: UUID, person_in: PersonUpdate) -> Person:
        """
        Update a person record by SID.

        :param sid: UUID of the target person.
        :param person_in: Updated person fields.
        :return: Updated person data.
        """
        ...

    @abstractmethod
    async def soft_delete(self, sid: UUID) -> Msg:
        """
        Soft delete a person record by SID.

        :param sid: UUID of the target person.
        :return: Confirmation message.
        """
        ...
