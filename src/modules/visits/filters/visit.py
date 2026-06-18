from datetime import datetime

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from src.common.constants.enums import LanguageEnum
from src.common.schemas import SQLFilterBase
from src.modules.visits.constants.enums import VisitStatusEnum, VisitFinishReasonEnum, \
    VisitHandoffReasonEnum
from src.modules.visits.models import VisitModel


class VisitFilter(SQLFilterBase):
    status: VisitStatusEnum | None = None
    finish_reason: VisitFinishReasonEnum | None = Field(None, alias="finishReason")
    handoff_reason: VisitHandoffReasonEnum | None = Field(None, alias="handoffReason")
    dialogue_lang: LanguageEnum | None = Field(None, alias="dialogueLang")
    granted_access: bool | None = Field(None, alias="grantedAccess")
    bot_granted_access: bool | None = Field(None, alias="botGrantedAccess")
    start_datetime__lt: datetime | None = Field(None, alias="startDatetimeTo")
    start_datetime__gt: datetime | None = Field(None, alias="startDatetimeFrom")

    class Constants(Filter.Constants):
        model = VisitModel


class VisitFilterFull(VisitFilter):
    status__in: list[VisitStatusEnum] | None = None
    call_employee_datetime__lt: datetime | None = None
