from __future__ import annotations

from dataclasses import Field
from uuid import UUID, uuid4

from src.common.schemas import CoreSchema
from src.common.constants.enums import GenderEnum
from src.modules.visits.constants.enums import VisitStatusEnum


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


class Visit(CoreSchema):
    sid: UUID
    status: VisitStatusEnum
