from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Body
from fastapi_filter import FilterDepends

from src.common.deps import get_user_sid
from src.common.schemas import ListResult, PaginationResult, Msg, Pagination, SortBase
from src.modules.visits.constants.enums import VisitSortFieldsEnum
from src.modules.visits.controllers.constants import VisitCtrlEnums
from src.modules.visits.interfaces import IVisitController


class VisitController(IVisitController):
    """FastAPI controller for managing meets.

    Handles all visits-related operations including CRUD and membership management.
    """

    def __init__(
        self,
        enums: VisitCtrlEnums,
    ):
        """Initialize the visit controller.

        :param enums: Controller enums containing paths and request types
        """
        self._controller = APIRouter()
        self._enums = enums
        self._add_controllers()

    @property
    def controller(self) -> APIRouter:
        """Get the configured APIRouter instance.

        :return: Configured FastAPI router with all visits routes
        """
        return self._controller

    def _add_controllers(self) -> None:
        """Register all common visits endpoints to the router."""
        ...

    @staticmethod
    def get_visit(
        sid: UUID,
        user_sid: Annotated[UUID, Depends(get_user_sid)],
        visit_usecase: Annotated[IVisitUC, Depends(get_visit_usecase)],
    ) -> VisitFull:
        """
        Get full info about visit by its identifier.

        ## Notes:
        - Is available for Administrator only.
        """
        ...

    @staticmethod
    def get_all_visits(
        user_sid: Annotated[UUID, Depends(get_user_sid)],
        sort_schema: SortBase[VisitSortFieldsEnum], # TODO: см как выглядит в сваггере
        filter_fields: Annotated[VisitFilter, FilterDepends(VisitFilter)],
        pagination_params: Annotated[Pagination, Depends(Pagination)],
        visit_usecase: Annotated[IVisitUC, Depends(get_visit_usecase)],
    ) -> PaginationResult[Visit]:
        """
        Get paginated visits list with optional filters and sorts.

        ## Returns:
        - Paginated list of visits.

        ## Notes:
        - Is available for Administrator only.
        """
        ...

    @staticmethod
    def get_waiting_decision_visits(
        visit_usecase: Annotated[IVisitUC, Depends(get_visit_usecase)],
    ) -> ListResult[VisitReport]:
        """
        Get the waiting decision visits list.

        ## Returns:
        - List of visits with 'waiting decision' status with full information for
        each: photo, visitors list, bot access decision, goal of the visit, etc.

        ## Notes:
        - Visits are sorted by startDatetime from oldest to newest.
        """
        ...

    @staticmethod
    def make_door_open_decision(
        user_sid: Annotated[UUID, Depends(get_user_sid)],
        door_open: Annotated[
            bool, Body(alias="doorOpen", validation_alias="doorOpen", embed=True)
        ],
        visit_usecase: Annotated[IVisitUC, Depends(get_visit_usecase)],
    ) -> Msg:
        """
        Make door open decision.

        ## Returns:
        - Operation result message.
        """
        ...
