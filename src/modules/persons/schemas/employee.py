from __future__ import annotations

from uuid import UUID

from src.common.decorators import partial_schema
from src.common.schemas import CoreSchema


class EmployeeBase(CoreSchema):
    full_name: str


class EmployeeCreate(EmployeeBase):
    pass


@partial_schema
class EmployeeUpdate(EmployeeBase):
    photo: str
    face_embedding: list[float]


class Employee(EmployeeBase):
    sid: UUID
    photo: str
