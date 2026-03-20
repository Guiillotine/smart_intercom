import typing

from src.common.schemas import CoreSchema

if typing.TYPE_CHECKING:
    from src.common.constants.enums import LanguageEnum


class SpeechInfo(CoreSchema):
    lang: LanguageEnum
    text: str


class AudioData(CoreSchema):
    s3_path: str
