import logging
from datetime import datetime
from uuid import UUID

from src.common.constants import ErrorCodesEnums
from src.common.errors import BackendException
from src.common.schemas import ListResult, Msg, Pagination, PaginationResult, SortBase
from src.modules.visits.constants.enums import VisitStatusEnum
from src.modules.visits.interfaces import IVisitPostgresRepo, IVisitSrv
from src.modules.visits.services.constants import VisitSrvConsts, VisitSrvEnums
from src.modules.visits.schemas import (
    Visit,
    VisitCallEmployee,
    VisitCreate,
    VisitFinish,
    VisitFull,
    VisitReport,
    VisitUpdate,
)


class VisitSrv(IVisitSrv):
    def __init__(
        self,
        errors: ErrorCodesEnums,
        enums: VisitSrvEnums,
        consts: VisitSrvConsts,
        logger: logging.Logger,
        visit_repo: IVisitPostgresRepo,
    ):
        self._errors = errors
        self._enums = enums
        self._consts = consts
        self._logger = logger
        self._visit_repo = visit_repo

    async def create_visit(self, visit_in: VisitCreate | None = None) -> Visit:
        return Visit.model_validate(
            await self._visit_repo.create(obj_in=visit_in or VisitCreate())
        )

    async def get_by_sid(self, sid: UUID) -> Visit:
        return Visit.model_validate(await self._get_model_by_sid(sid))

    async def get_full_by_sid(self, sid: UUID) -> VisitFull:
        return VisitFull.model_validate(await self._get_model_by_sid(sid))

    async def get_all_paginated(
        self,
        pagination_params: Pagination,
        filters=None,
        sort_params: SortBase = None,
    ) -> PaginationResult[Visit]:
        visits, total = await self._visit_repo.get_all_paginated(
            pagination_params=pagination_params,
            filters=filters,
            sort_params=sort_params,
        )
        return PaginationResult(
            items=[Visit.model_validate(visit) for visit in visits],
            limit=pagination_params.limit,
            offset=pagination_params.offset,
            total=total,
        )

    async def get_waiting_decision_visits(self) -> ListResult[VisitReport]:
        visits = await self._visit_repo.get_all()
        return ListResult(
            items=[
                VisitReport.model_validate(visit)
                for visit in visits
                if visit.status == VisitStatusEnum.WAITING_DECISION
            ]
        )

    async def update_visit(self, sid: UUID, visit_in: VisitUpdate) -> Visit:
        visit = await self._get_model_by_sid(sid)
        return Visit.model_validate(
            await self._visit_repo.update(db_obj=visit, obj_in=visit_in)
        )

    async def call_employee(
        self,
        sid: UUID,
        visit_call_employee_params: VisitCallEmployee | None = None,
    ) -> Visit:
        params = visit_call_employee_params or VisitCallEmployee()
        return await self.update_visit(
            sid=sid,
            visit_in=VisitUpdate(
                status=VisitStatusEnum.WAITING_DECISION,
                visitor_goal=params.visitor_goal,
                bot_granted_access=params.bot_granted_access,
            ),
        )

    async def finish_visit(
        self,
        sid: UUID,
        visit_finish_params: VisitFinish | None = None,
    ) -> Visit:
        params = visit_finish_params or VisitFinish()
        return await self.update_visit(
            sid=sid,
            visit_in=VisitUpdate(
                status=VisitStatusEnum.OVER,
                finish_datetime=datetime.utcnow(),
                visitor_goal=params.visitor_goal,
                bot_granted_access=params.bot_granted_access,
            ),
        )

    async def make_door_open_decision(
        self, sid: UUID, user_sid: UUID, door_open: bool
    ) -> Msg:
        await self.update_visit(
            sid=sid,
            visit_in=VisitUpdate(
                granted_access=door_open,
                decision_by_user_sid=user_sid,
                status=VisitStatusEnum.OVER,
                finish_datetime=datetime.utcnow(),
            ),
        )
        return Msg()

    async def _get_model_by_sid(self, sid: UUID):
        visit = await self._visit_repo.get_by_sid(sid)
        if not visit:
            raise BackendException(error=self._errors.Common.NOT_FOUND)
        return visit
