import logging
from datetime import datetime, UTC
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.sql.base import ExecutableOption

from src.common.constants import ErrorCodesEnums
from src.common.constants.srv_req_enums import VisitRequirementsEnum
from src.common.decorators import LoggingFunctionInfo
from src.common.errors import BackendException
from src.common.schemas import ListResult, Msg, Pagination, PaginationResult, SortBase
from src.config.settings import Settings
from src.modules.visits.constants.enums import VisitStatusEnum, VisitHandoffReasonEnum, \
    VisitFinishReasonEnum
from src.modules.visits.filters.visit import VisitFilter
from src.modules.visits.interfaces import IVisitPostgresRepo, IVisitSrv, \
    IVisitPersonPostgresRepo, IVisitS3Repo
from src.modules.visits.models import VisitModel
from src.modules.visits.services.constants import VisitSrvConsts, VisitSrvEnums
from src.modules.visits.schemas import (
    Visit,
    VisitCreate,
    VisitReport,
    VisitUpdate, VisitPersonCreate, VisitPerson, VisitPhotoResponse,
)
from src.modules.visits.services.constants.consts import VisitRespSchemas


class VisitSrv(IVisitSrv):
    def __init__(
        self,
        errors: ErrorCodesEnums,
        enums: VisitSrvEnums,
        consts: VisitSrvConsts,
        logger: logging.Logger,
        settings: Settings,
        visit_pg_repo: IVisitPostgresRepo,
        visit_s3_repo: IVisitS3Repo,
        visit_person_pg_repo: IVisitPersonPostgresRepo,
    ):
        self._errors = errors
        self._enums = enums
        self._consts = consts
        self._logger = logger
        self._visit_photo_bucket_name = settings.s3.VISIT_PHOTO_BUCKET_NAME
        self._visit_pg_repo = visit_pg_repo
        self._visit_s3_repo = visit_s3_repo
        self._visit_person_pg_repo = visit_person_pg_repo

    @LoggingFunctionInfo(description="Get visit by identifier.")
    async def get_by_sid(
        self,
        sid: UUID,
        requirement: VisitRequirementsEnum | None = None,
    ) -> VisitRespSchemas.GET_BY_SID:
        if not requirement:
            requirement = self._enums.SrvReqCommon.VisitRequirements.EMPTY

        custom_options = self._consts.Requirements.GET_BY_SID.get(requirement).get(
            self._enums.SrvReqCommon.RequirementFieldName.OPTIONS
        )()

        visit = await self._get_model_by_sid(sid, custom_options=custom_options)
        if requirement == self._enums.SrvReqCommon.VisitRequirements.WITH_MESSAGES:
            visit.messages = sorted(visit.messages, key=lambda msg: msg.time)

        response_schema = self._consts.Requirements.GET_BY_SID.get(requirement).get(
            self._enums.SrvReqCommon.RequirementFieldName.RESPONSE_SCHEMA
        )

        return response_schema.model_validate(visit)

    @LoggingFunctionInfo(description="Get all visits.")
    async def get_all(
        self,
        filters: VisitFilter | None = None,
        sort_params: SortBase | None = None,
        requirement: VisitRequirementsEnum | None = None,
    ) -> ListResult[VisitRespSchemas.GET_ALL]:
        if not requirement:
            requirement = self._enums.SrvReqCommon.VisitRequirements.EMPTY

        custom_options = self._consts.Requirements.GET_ALL.get(requirement).get(
            self._enums.SrvReqCommon.RequirementFieldName.OPTIONS
        )()

        visits = await self._visit_pg_repo.get_all(
            filters=filters,
            sort_params=sort_params,
            custom_options=custom_options,
        )

        response_schema = self._consts.Requirements.GET_ALL.get(requirement).get(
            self._enums.SrvReqCommon.RequirementFieldName.RESPONSE_SCHEMA
        )

        return ListResult[response_schema](items=visits)

    @LoggingFunctionInfo(description="Get paginated visits.")
    async def get_all_paginated(
        self,
        pagination_params: Pagination,
        filters=None,
        sort_params: SortBase = None,
    ) -> PaginationResult[Visit]:
        visits, total = await self._visit_pg_repo.get_all_paginated(
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

    @LoggingFunctionInfo(description="Get visits waiting for a door opening decision.")
    async def get_waiting_decision_visits(self) -> ListResult[VisitReport]:
        requirement = self._enums.SrvReqCommon.VisitRequirements.FULL
        custom_options = self._consts.Requirements.GET_ALL.get(requirement).get(
            self._enums.SrvReqCommon.RequirementFieldName.OPTIONS
        )()

        visits = await self._visit_pg_repo.get_all(custom_options=custom_options)

        return ListResult[VisitReport](
            items=[
                VisitReport.model_validate(visit)
                for visit in visits
                if visit.status == VisitStatusEnum.WAITING_DECISION
            ]
        )

    @LoggingFunctionInfo(description="Create a visit.")
    async def create_visit(self, visit_in: VisitCreate) -> Visit:
        return Visit.model_validate(
            await self._visit_pg_repo.create(obj_in=visit_in)
        )

    @LoggingFunctionInfo(description="Create a visitor.")
    async def create_visitor(self, visit_person_in: VisitPersonCreate) -> VisitPerson:
        return VisitPerson.model_validate(
            await self._visit_person_pg_repo.create(obj_in=visit_person_in)
        )

    @LoggingFunctionInfo(description="Upload visit photo.")
    async def save_visit_photo(
        self,
        sid: UUID,
        photo: UploadFile,
    ) -> VisitPhotoResponse:
        visit = await self._get_model_by_sid(sid)

        if visit.photo_s3_path is not None:
            await self._delete_visit_photo(key=visit.photo_s3_path)

        key = f"{self._enums.Common.S3Prefix.VISIT}/{sid}/{photo.filename}"
        self._logger.debug("Uploading photo with key: %s", key)

        key = await self._visit_s3_repo.put_object(
            bucket=self._visit_photo_bucket_name,
            key=key,
            data=await photo.read(),
        )

        path = await self._update_visit_photo(key=key, visit=visit)

        return VisitPhotoResponse(path=path)

    @LoggingFunctionInfo(description="Update a visit.")
    async def update_visit(self, sid: UUID, visit_in: VisitUpdate) -> Visit:
        visit = await self._get_model_by_sid(sid)
        return Visit.model_validate(
            await self._visit_pg_repo.update(db_obj=visit, obj_in=visit_in)
        )

    @LoggingFunctionInfo(description="Move visit to employee decision state.")
    async def call_employee(
        self,
        sid: UUID,
        reason: VisitHandoffReasonEnum,
    ) -> Visit:
        return await self.update_visit(
            sid=sid,
            visit_in=VisitUpdate(
                status=VisitStatusEnum.WAITING_DECISION,
                handoff_reason=reason,
            ),
        )

    @LoggingFunctionInfo(description="Set visit status to 'asked wanted to enter'.")
    async def ask_want_to_enter(
        self,
        sid: UUID,
    ) -> Visit:
        return await self.update_visit(
            sid=sid,
            visit_in=VisitUpdate(status=VisitStatusEnum.ASKED_WANT_TO_ENTER),
        )

    @LoggingFunctionInfo(description="Finish a visit.")
    async def finish_visit(
        self,
        sid: UUID,
        finish_reason: VisitFinishReasonEnum,
    ) -> Visit:
        return await self.update_visit(
            sid=sid,
            visit_in=VisitUpdate(
                status=VisitStatusEnum.OVER,
                finish_datetime=datetime.now(UTC),
                finish_reason=finish_reason,
            ),
        )

    @LoggingFunctionInfo(description="Persist user door opening decision.")
    async def make_door_open_decision(
        self, sid: UUID, user_sid: UUID, door_open: bool
    ) -> Msg:
        await self.update_visit(
            sid=sid,
            visit_in=VisitUpdate(
                granted_access=door_open,
                decision_by_user_sid=user_sid,
            ),
        )
        return Msg()

    @LoggingFunctionInfo(description="Delete visit by identifier.")
    async def delete_visit(self, sid) -> Msg:
        await self._visit_pg_repo.delete(sid=sid)
        return Msg()

    async def _get_model_by_sid(
        self,
        sid: UUID,
        custom_options: tuple[ExecutableOption, ...] = None,
    ) -> VisitModel:
        visit = await self._visit_pg_repo.get_by_sid(sid, custom_options=custom_options)
        if not visit:
            raise BackendException(error=self._errors.Visit.VISIT_NOT_FOUND)
        return visit

    @LoggingFunctionInfo(description="Update visit photo path in the database.")
    async def _update_visit_photo(
        self,
        key: str,
        visit: VisitModel,
    ) -> str:
        self._logger.debug("Updating photo for visit: %s", visit.sid)
        photo_s3_path = f"{self._visit_photo_bucket_name}/" + key

        obj_in = VisitUpdate(photo_s3_path=photo_s3_path)
        await self._visit_pg_repo.update(db_obj=visit, obj_in=obj_in)

        return photo_s3_path

    @LoggingFunctionInfo(description="Delete visit photo from S3 storage.")
    async def _delete_visit_photo(self, key: str) -> None:
        key = key.replace(f"{self._visit_photo_bucket_name}/", "/")

        self._logger.debug("Deleting photo with key: %s", key)
        await self._visit_s3_repo.delete_object(
            bucket=self._visit_photo_bucket_name, key=key
        )
