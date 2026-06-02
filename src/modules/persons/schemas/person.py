from __future__ import annotations

from uuid import UUID, uuid4

from pydantic import Field

from src.common.decorators import partial_schema
from src.common.schemas import CoreSchema
from src.modules.persons.constants.enums import PersonTypeEnum


class PersonBase(CoreSchema):
    first_name: str
    last_name: str
    middle_name: str | None = None
    photo_s3_path: str


class PersonCreate(PersonBase):
    person_type: PersonTypeEnum | None = None
    face_embedding: list[float]


@partial_schema
class PersonUpdate(PersonBase):
    is_archived: bool
    face_embedding: list[float]


class PersonShort(PersonBase):
    sid: UUID
    person_type: PersonTypeEnum


class Person(PersonShort):
    face_embedding: list[float]


class PersonPhotoResponse(CoreSchema):
    path: str
