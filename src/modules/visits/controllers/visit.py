from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Body, Path
from fastapi_filter import FilterDepends

from src.common.deps import get_user_sid, require_admin
from src.common.schemas import ListResult, PaginationResult, Msg, Pagination, SortBase
from src.modules.visits.constants.enums import VisitSortFieldsEnum
from src.modules.visits.controllers.constants import VisitCtrlEnums
from src.modules.visits.filters.visit import VisitFilterFull, VisitFilter
from src.modules.visits.interfaces import IVisitController
from src.modules.visits.interfaces.usecases import IVisitUC
from src.modules.visits.schemas import VisitReport, VisitFull, Visit
from src.modules.visits.usecases.deps import get_visit_usecase


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
        self._controller.add_api_route(
            path=self._enums.VisitCtrlPath.get_all_visits,
            endpoint=self.get_all_visits,
            methods=[self._enums.Common.RequestType.GET],
            response_model=PaginationResult[Visit],
        )

        self._controller.add_api_route(
            path=self._enums.VisitCtrlPath.get_waiting_decision_visits,
            endpoint=self.get_waiting_decision_visits,
            methods=[self._enums.Common.RequestType.GET],
            response_model=ListResult[VisitReport],
        )

        self._controller.add_api_route(
            path=self._enums.VisitCtrlPath.get_visit,
            endpoint=self.get_visit,
            methods=[self._enums.Common.RequestType.GET],
            response_model=VisitFull,
        )

        self._controller.add_api_route(
            path=self._enums.VisitCtrlPath.make_door_open_decision,
            endpoint=self.make_door_open_decision,
            methods=[self._enums.Common.RequestType.POST],
            response_model=Msg,
        )

    @staticmethod
    async def get_visit(
        sid: Annotated[UUID, Path()],
        user_sid: Annotated[UUID, Depends(require_admin)],
        visit_usecase: Annotated[IVisitUC, Depends(get_visit_usecase)],
    ) -> VisitFull:
        """
        Get full info about visit by its identifier.

        ## Notes:
        - Is available for Administrator only.
        """
        return await visit_usecase.get_visit(
            sid=sid,
            user_sid=user_sid,
        )

    @staticmethod
    async def get_all_visits(
        user_sid: Annotated[UUID, Depends(require_admin)],
        sort_schema: Annotated[
            SortBase, Depends(SortBase[VisitSortFieldsEnum])
        ],
        filter_fields: Annotated[VisitFilterFull, FilterDepends(VisitFilter)],
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
        return await visit_usecase.get_all_visits(
            user_sid=user_sid,
            sort_schema=sort_schema,
            filter_fields=filter_fields,
            pagination_params=pagination_params,
        )

    @staticmethod
    async def get_waiting_decision_visits(
        user_sid: Annotated[UUID, Depends(get_user_sid)],
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
        return await visit_usecase.get_waiting_decision_visits()

    @staticmethod
    async def make_door_open_decision(
        sid: Annotated[UUID, Path()],
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
        return await visit_usecase.make_door_open_decision(
            sid=sid,
            user_sid=user_sid,
            door_open=door_open,
        )
