from __future__ import annotations

from uuid import UUID, uuid4

from pydantic import Field

from src.common.decorators import partial_schema
from src.common.schemas import CoreSchema
from src.modules.persons.constants.enums import PersonTypeEnum


class PersonBase(CoreSchema):
    photo: str
    full_name: str | None = None
    face_embedding: list[float]


class PersonCreate(PersonBase):
    person_type: PersonTypeEnum | None = None


@partial_schema
class PersonUpdate(PersonBase):
    is_archived: bool


class Person(PersonBase):
    sid: UUID
    person_type: PersonTypeEnum
