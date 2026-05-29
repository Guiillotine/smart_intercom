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
    face_embedding: list[float]


class PersonCreate(PersonBase):
    person_type: PersonTypeEnum | None = None


@partial_schema
class PersonUpdate(PersonBase):
    is_archived: bool


class Person(PersonBase):
    sid: UUID
    person_type: PersonTypeEnum


class PersonPhotoResponse(CoreSchema):
    path: str
