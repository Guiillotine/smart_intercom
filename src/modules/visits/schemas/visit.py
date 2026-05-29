from __future__ import annotations

from datetime import datetime
from uuid import UUID

from src.common.decorators import partial_schema
from src.common.schemas import CoreSchema
from src.common.constants.enums import GenderEnum, LanguageEnum
from src.modules.messages.schemas import Message
from src.modules.persons.schemas import Person
from src.modules.visits.constants.enums import VisitStatusEnum, VisitFinishReasonEnum, \
    VisitHandoffReasonEnum


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


class VisitPersonFull(VisitPerson):
    person: Person | None


# Visit


class VisitBase(CoreSchema):
    status: VisitStatusEnum
    start_datetime: datetime
    dialogue_lang: LanguageEnum


class VisitCreate(VisitBase):
    photo_s3_path: str | None = None


@partial_schema
class VisitUpdate(VisitBase):
    photo_s3_path: str
    visitor_goal: str
    granted_access: bool
    finish_datetime: datetime
    bot_granted_access: bool
    decision_by_user_sid: UUID
    finish_reason: VisitFinishReasonEnum
    handoff_reason: VisitHandoffReasonEnum


class Visit(VisitBase):
    sid: UUID
    visitor_goal: str | None = None
    finish_datetime: datetime | None = None
    photo_s3_path: str | None
    granted_access: bool | None = None
    bot_granted_access: bool | None = None
    finish_reason: VisitFinishReasonEnum | None = None
    handoff_reason: VisitHandoffReasonEnum | None = None


class VisitWithMessages(Visit):
    messages: list[Message]


class VisitFull(VisitWithMessages):
    visitors: list[VisitPersonFull]


class VisitReport(VisitFull):
    pass


class VisitPhotoResponse(CoreSchema):
    path: str
