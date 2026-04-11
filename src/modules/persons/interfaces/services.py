from abc import ABC, abstractmethod
from uuid import UUID

from src.common.schemas import Msg, Pagination, PaginationResult
from src.modules.persons.schemas import PersonCreate, PersonUpdate, Person


class IPersonSrv(ABC):
    """
    Interface for shared person service operations.
    """

    @abstractmethod
    async def get_all(
        self,
        pagination_params: Pagination,
    ) -> PaginationResult[Person]:
        """
        Retrieve a paginated list of persons.

        :param pagination_params: Pagination settings.
        :param person_type: Optional person type identifier.
        :return: Paginated list of persons.
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
    async def delete(self, sid: UUID) -> Msg:
        """
        Delete a person record by SID.

        :param sid: UUID of the target person.
        :return: Confirmation message.
        """
        ...
