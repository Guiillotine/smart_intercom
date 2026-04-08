from __future__ import annotations

from dataclasses import Field
from datetime import datetime
from uuid import UUID, uuid4

from src.common.schemas import CoreSchema
from src.common.constants.enums import GenderEnum
from src.modules.visits.constants.enums import VisitStatusEnum, VisitFinishReasonEnum


class VisitPersonBase(CoreSchema):
    visit_sid: UUID
    person_sid: UUID
    detected_age: int
    detected_sex: GenderEnum
    photo: str


class VisitPersonCreate(VisitPersonBase):
    pass


class VisitPerson(VisitPersonBase):
    sid: UUID = Field(default_factory=uuid4) # TODO: временное решение


class VisitBase(CoreSchema):
    status: VisitStatusEnum
    start_datetime: datetime


class VisitUpdate(CoreSchema):
    status: VisitStatusEnum | None = None
    visitor_goal: str | None = None
    start_datetime: datetime | None = None
    finish_datetime: datetime | None = None
    bot_granted_access: bool | None = None
    finish_reason: VisitFinishReasonEnum | None = None


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
