from __future__ import annotations

from uuid import UUID, uuid4

from pydantic import Field

from src.common.schemas import CoreSchema
from src.modules.persons.constants.enums import PersonTypeEnum


class PersonInfoBase(CoreSchema):
    full_name: str | None = None
    photo: str
    person_type: PersonTypeEnum


class PersonInfoCreate(PersonInfoBase):
    face_embedding: list[float]


class PersonInfo(PersonInfoBase):
    sid: UUID = Field(default_factory=uuid4) # TODO: временное решение
    face_embedding: list[float]
