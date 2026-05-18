from enum import IntEnum


class DialogueModeEnum(IntEnum):
    DETECT_LANGUAGE = 0
    VISITOR_CALL_EMPLOYEE = 1
    GOAL = 2
    GRANT_ACCESS = 3
    WANT_TO_ENTER = 4


class DialogueEnums:
    def __init__(self):
        self.DialogueMode = DialogueModeEnum
