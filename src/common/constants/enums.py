from enum import StrEnum, IntEnum, auto


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

    @classmethod
    def get_langs_str_list(cls) -> str:
      langs = [f"\"{lang.value}\"" for lang in cls]
      return ", ".join(langs)


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


class S3PrefixEnum(StrEnum):
    """Enum defining S3 object key prefixes for different resource types."""

    VISIT = "visits"
    PERSON = "persons/employees"
    BOT_MESSAGE = "bot_messages"


class CommonEnums:
    def __init__(self):
        self.Gender = GenderEnum
        self.Language = LanguageEnum
        self.S3Prefix = S3PrefixEnum
        self.RequestType = RequestTypeEnum
        self.MessageAuthorRole = MessageAuthorRoleEnum
