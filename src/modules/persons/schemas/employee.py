from __future__ import annotations

from uuid import UUID

from src.common.decorators import partial_schema
from src.common.schemas import CoreSchema


class EmployeeBase(CoreSchema):
    first_name: str
    last_name: str
    middle_name: str | None = None


class EmployeeCreate(EmployeeBase):
    pass


@partial_schema
class EmployeeUpdate(EmployeeBase):
    photo_s3_path: str
    face_embedding: list[float]


class Employee(EmployeeBase):
    sid: UUID
    photo_s3_path: str
