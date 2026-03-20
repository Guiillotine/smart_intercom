from enum import StrEnum, IntEnum


class RequestTypeEnum(StrEnum):
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"


class LanguageEnum(StrEnum):
    RU = "ru"
    EN = "en"

    @classmethod
    def get_all_langs(cls) -> list[str]:
      return [lang.value for lang in cls]


class MessageAuthorRoleEnum(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class GenderEnum(IntEnum):
    """
    1: FEMALE
    2: MALE
    """
    FEMALE = 0
    MALE = 1


class CommonEnums:
    def __init__(self):
        self.Gender = GenderEnum
        self.Language = LanguageEnum
        self.RequestType = RequestTypeEnum
        self.MessageAuthorRole = MessageAuthorRoleEnum
