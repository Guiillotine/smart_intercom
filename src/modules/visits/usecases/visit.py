from uuid import UUID

from src.common.schemas import ListResult, Msg, Pagination, PaginationResult, SortBase
from src.modules.visits.filters.visit import VisitFilter
from src.modules.visits.interfaces import IVisitSrv, IVisitUC
from src.modules.visits.schemas import Visit, VisitFull, VisitReport
from src.modules.visits.usecases.constants import VisitUCConsts, VisitUCEnums


class VisitUC(IVisitUC):
    def __init__(
        self,
        enums: VisitUCEnums,
        consts: VisitUCConsts,
        visit_service: IVisitSrv,
    ):
        self._enums = enums
        self._consts = consts
        self._visit_service = visit_service

    async def get_visit(self, sid: UUID, user_sid: UUID) -> VisitFull:
        return await self._visit_service.get_by_sid(
            sid,
            requirement=self._enums.SrvReqCommon.VisitRequirements.FULL,
        )

    async def get_all_visits(
        self,
        user_sid: UUID,
        pagination_params: Pagination,
        filter_fields=None,
        sort_schema: SortBase = None,
    ) -> PaginationResult[Visit]:
        return await self._visit_service.get_all_paginated(
            pagination_params=pagination_params,
            filters=filter_fields,
            sort_params=sort_schema,
        )

    async def get_waiting_decision_visits(self) -> ListResult[VisitReport]:
        return await self._visit_service.get_waiting_decision_visits(

        )

    async def make_door_open_decision(
        self, sid: UUID, user_sid: UUID, door_open: bool
    ) -> Msg:
        await self._visit_service.make_door_open_decision(
            sid=sid, user_sid=user_sid, door_open=door_open
        )

        await self._visit_service.finish_visit(
            sid,
            finish_reason=self._enums.Visit.FinishReason.EMPLOYEE_DECISION,
        )

        return Msg()

    async def finish_waiting_decision_visits(self) -> None:
        visits = await self._visit_service.get_all(
            filters=VisitFilter(
                status=self._enums.Visit.Status.WAITING_DECISION,
                call_employee_datetime__lt=0# TODO: now - max_waiting_min,
            )
        )
        for visit in visits.items:
            await self._visit_service.finish_visit(
                visit.sid,
                finish_reason=self._enums.Visit.FinishReason.WAITING_DECISION_TIMEOUT,
            )
