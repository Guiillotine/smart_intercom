from __future__ import annotations

from src.common.schemas import CoreSchema
from src.common.constants.enums import LanguageEnum


class SpeechInfo(CoreSchema):
    lang: LanguageEnum
    text: str


class AudioData(CoreSchema):
    s3_path: str


class TTSModelParams(CoreSchema):
    model_id: str
    speaker: str
