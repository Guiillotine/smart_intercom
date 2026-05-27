from enum import IntEnum, StrEnum, auto

from src.common.constants import CommonEnums


class DialogueModeEnum(IntEnum):
    DETECT_LANGUAGE = 0
    VISITOR_CALL_EMPLOYEE = 1
    GOAL = 2
    GRANT_ACCESS = 3
    WANT_TO_ENTER = 4


class BotMessageEnum(StrEnum):
  HELLO = auto()
  ERROR = auto()
  RECOGNIZED = auto()
  ACCESS_GRANTED = auto()
  ACCESS_NOT_GRANTED = auto()
  WANT_TO_ENTER_QUESTION = auto()
  CALL_EMPLOYEE = auto()
  GOODBYE = auto()


class DialogueEnums:
    def __init__(
        self,
        common_enums: CommonEnums,
    ):
        self.Common = common_enums
        self.BotMessage = BotMessageEnum
        self.DialogueMode = DialogueModeEnum
