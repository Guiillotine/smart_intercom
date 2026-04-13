from __future__ import annotations

from uuid import UUID

from src.common.decorators import partial_schema
from src.common.schemas import CoreSchema


class EmployeeBase(CoreSchema):
    full_name: str
    photo: str


class EmployeeCreate(EmployeeBase):
    face_embedding: list[float]


@partial_schema
class EmployeeUpdate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    sid: UUID
