import logging
from datetime import timedelta
from uuid import UUID

from src.common.interfaces import ICustomDateTime
from src.common.schemas import ListResult, Msg, Pagination, PaginationResult, SortBase
from src.config.settings import Settings
from src.modules.visits.filters.visit import VisitFilterFull, VisitFilter
from src.modules.visits.interfaces import IVisitSrv, IVisitUC
from src.modules.visits.schemas import Visit, VisitFull, VisitReport
from src.modules.visits.usecases.constants import VisitUCConsts, VisitUCEnums


class VisitUC(IVisitUC):
    def __init__(
        self,
        logger: logging.Logger,
        enums: VisitUCEnums,
        consts: VisitUCConsts,
        settings: Settings,
        custom_datetime: ICustomDateTime,
        visit_service: IVisitSrv,
    ):
        self._logger = logger
        self._enums = enums
        self._consts = consts
        self._visit_service = visit_service
        self._custom_datetime = custom_datetime
        self.max_waiting_decision_time_sec = (
            settings.project.MAX_WAITING_DECISION_TIME_SEC
        )
    async def get_visit(self, sid: UUID, user_sid: UUID) -> VisitFull:
        return await self._visit_service.get_by_sid(
            sid,
            requirement=self._enums.SrvReqCommon.VisitRequirements.FULL,
        )

    async def get_all_visits(
        self,
        user_sid: UUID,
        filter_fields: VisitFilter,
        pagination_params: Pagination,
        sort_schema: SortBase = None,
    ) -> PaginationResult[Visit]:
        return await self._visit_service.get_all_paginated(
            filters=VisitFilterFull.model_validate(
                filter_fields.model_dump(exclude_none=True)
            ),
            sort_params=sort_schema,
            pagination_params=pagination_params,
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
        now = self._custom_datetime.get_utc_datetime()
        timeout_threshold = now - timedelta(
            seconds=self.max_waiting_decision_time_sec,
        )

        visits = await self._visit_service.get_all(
            filters=VisitFilterFull(
                status=self._enums.Visit.Status.WAITING_DECISION,
                call_employee_datetime__lt=timeout_threshold,
            ),
        )

        finished_visits = 0
        for visit in visits.items:
            await self._visit_service.finish_visit(
                visit.sid,
                finish_reason=self._enums.Visit.FinishReason.WAITING_DECISION_TIMEOUT,
            )
            finished_visits+=1
        self._logger.info(
            f"Finished visits: {finished_visits} cause of waiting decision timeout"
        )
