from __future__ import annotations

from uuid import UUID, uuid4

from pydantic import Field

from src.common.schemas import CoreSchema
from src.modules.persons.constants.enums import PersonTypeEnum


class PersonBase(CoreSchema):
    full_name: str | None = None
    photo: str


class PersonCreate(PersonBase):
    face_embedding: list[float]
    person_type: PersonTypeEnum | None = None


@partial_schema
class PersonUpdate(PersonBase):
    pass


class Person(PersonBase):
    sid: UUID = Field(default_factory=uuid4) # TODO: временное решение
    face_embedding: list[float]
    person_type: PersonTypeEnum
