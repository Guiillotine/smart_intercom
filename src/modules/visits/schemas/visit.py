from __future__ import annotations

from dataclasses import Field
from datetime import datetime, UTC
from uuid import UUID, uuid4

from src.common.decorators import partial_schema
from src.common.schemas import CoreSchema
from src.common.constants.enums import GenderEnum, LanguageEnum
from src.modules.visits.constants.enums import VisitStatusEnum, VisitFinishReasonEnum


# Visit person


class VisitPersonBase(CoreSchema):
    visit_sid: UUID
    person_sid: UUID | None = None
    detected_age: int | None = None
    detected_sex: GenderEnum | None = None
    crop_coords: list[int]


class VisitPersonCreate(VisitPersonBase):
    pass


class VisitPerson(VisitPersonBase):
    sid: UUID


# Visit


class VisitBase(CoreSchema):
    status: VisitStatusEnum
    arrival_datetime: datetime
    dialog_lang: LanguageEnum


class VisitCreate(CoreSchema):
    status: VisitStatusEnum = VisitStatusEnum.IN_PROCESS
    start_datetime: datetime = Field(default_factory=datetime.now(UTC))
    dialog_lang: LanguageEnum = LanguageEnum.RU
    photo: str | None = None


@partial_schema
class VisitUpdateShort(CoreSchema):
    dialog_lang: LanguageEnum


class VisitUpdate(VisitUpdateShort):
    status: VisitStatusEnum
    visitor_goal: str
    start_datetime: datetime
    finish_datetime: datetime
    bot_granted_access: bool
    granted_access: bool
    photo: str
    decision_by_user_sid: UUID


class VisitCallEmployee(CoreSchema):
    visitor_goal: str | None = None
    bot_granted_access: bool | None = None
    finish_reason: VisitFinishReasonEnum | None = None


class VisitFinish(CoreSchema):
    finish_reason: VisitFinishReasonEnum
    visitor_goal: str | None = None
    bot_granted_access: bool | None = None


class Visit(CoreSchema):
    sid: UUID
    status: VisitStatusEnum
    visitor_goal: str | None = None
    finish_datetime: datetime | None = None
    bot_granted_access: bool | None = None
    finish_reason: VisitFinishReasonEnum | None = None
    dialog_lang: LanguageEnum


class VisitFull(Visit):
    visitors: list[VisitPerson] = Field(default_factory=list)
    messages: list = Field(default_factory=list)


class VisitReport(VisitFull):
    pass
