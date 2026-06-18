from abc import ABC, abstractmethod
from uuid import UUID

from src.common.schemas import ListResult, Msg, Pagination, PaginationResult, SortBase
from src.modules.visits.filters.visit import VisitFilterFull, VisitFilter
from src.modules.visits.schemas import Visit, VisitFull, VisitReport


class IVisitUC(ABC):
    """
    Interface for visit use case operations.

    Defines application-level workflows for visits.
    """

    @abstractmethod
    async def get_visit(self, sid: UUID, user_sid: UUID) -> VisitFull:
        """
        Get full visit information.

        :param sid: Visit identifier.
        :param user_sid: Current authorized user SID.
        :return: Full visit data.
        """
        ...

    @abstractmethod
    async def get_all_visits(
        self,
        user_sid: UUID,
        filter_fields: VisitFilter,
        pagination_params: Pagination,
        sort_schema: SortBase = None,
    ) -> PaginationResult[Visit]:
        """
        Get paginated visit list.

        :param user_sid: Current authorized user SID.
        :param pagination_params: Pagination parameters.
        :param filter_fields: Filter schema.
        :param sort_schema: Optional sorting parameters.
        :return: Paginated visit list.
        """
        ...

    @abstractmethod
    async def get_waiting_decision_visits(self) -> ListResult[VisitReport]:
        """
        Get visits waiting for a door opening decision.

        :return: List of visit reports.
        """
        ...

    @abstractmethod
    async def make_door_open_decision(
        self, sid: UUID, user_sid: UUID, door_open: bool
    ) -> Msg:
        """
        Make and persist a door opening decision.

        :param sid: Visit identifier.
        :param user_sid: Current authorized user SID.
        :param door_open: Whether the door should be opened.
        :return: Operation result message.
        """
        ...

    @abstractmethod
    async def finish_waiting_decision_visits(self) -> None:
        """
        Finish waiting decision visits cause of timeout.
        """
        ...
