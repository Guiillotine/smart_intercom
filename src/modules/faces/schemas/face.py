from __future__ import annotations

from src.common.schemas import CoreSchema
from src.common.constants.enums import GenderEnum


class FaceInfo(CoreSchema):
    detected_age: int | None = None
    detected_sex: GenderEnum | None = None
    face_embedding: list[float]
    crop_coords: list[int]
