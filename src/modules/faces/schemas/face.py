from __future__ import annotations

from numpy import ndarray

from src.common.schemas import CoreSchema
from src.common.constants.enums import GenderEnum


class FaceInfo(CoreSchema):
    detected_age: int
    detected_sex: GenderEnum
    photo: str
    face_embedding: list[float]
    crop: ndarray
