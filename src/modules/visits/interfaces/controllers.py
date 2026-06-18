from abc import ABC, abstractmethod
from uuid import UUID

from fastapi import APIRouter

from src.common.schemas import ListResult, Msg, Pagination, PaginationResult, SortBase
from src.modules.visits.constants.enums import VisitSortFieldsEnum
from src.modules.visits.filters.visit import VisitFilterFull, VisitFilter
from src.modules.visits.interfaces.usecases import IVisitUC
from src.modules.visits.schemas import Visit, VisitFull, VisitReport


class IVisitController(ABC):
    """
    Interface for visit controller operations.

    Defines the contract for all visit-related API endpoints.
    """

    @property
    @abstractmethod
    def controller(self) -> APIRouter:
        """
        Get the configured APIRouter instance.

        :return: Configured FastAPI router with all visit routes.
        """
        ...

    @staticmethod
    @abstractmethod
    async def get_visit(
        sid: UUID,
        user_sid: UUID,
        visit_usecase: IVisitUC,
    ) -> VisitFull:
        """
        Get full visit information by identifier.

        :param sid: Visit identifier.
        :param user_sid: Current authorized user SID.
        :param visit_usecase: Visit use case dependency.
        :return: Full visit data.
        """
        ...

    @staticmethod
    @abstractmethod
    async def get_all_visits(
        user_sid: UUID,
        sort_schema: SortBase[VisitSortFieldsEnum],
        filter_fields: VisitFilter,
        pagination_params: Pagination,
        visit_usecase: IVisitUC,
    ) -> PaginationResult[Visit]:
        """
        Get paginated visits list.

        :param user_sid: Current authorized user SID.
        :param pagination_params: Pagination parameters.
        :param visit_usecase: Visit use case dependency.
        :param sort_schema: Optional sorting parameters.
        :param filter_fields: Filter fields.
        :return: Paginated visit list.
        """
        ...

    @staticmethod
    @abstractmethod
    async def get_waiting_decision_visits(
        user_sid: UUID,
        visit_usecase: IVisitUC,
    ) -> ListResult[VisitReport]:
        """
        Get visits waiting for user decision.

        :param user_sid: Current authorized user SID.
        :param visit_usecase: Visit use case dependency.
        :return: List of visits waiting for decision.
        """
        ...

    @staticmethod
    @abstractmethod
    async def make_door_open_decision(
        sid: UUID,
        user_sid: UUID,
        door_open: bool,
        visit_usecase: IVisitUC,
    ) -> Msg:
        """
        Save a door opening decision for a visit.

        :param sid: Visit identifier.
        :param user_sid: Current authorized user SID.
        :param door_open: Whether the door should be opened.
        :param visit_usecase: Visit use case dependency.
        :return: Operation result message.
        """
        ...
