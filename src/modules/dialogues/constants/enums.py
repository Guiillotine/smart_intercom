from enum import IntEnum


class DialogueModeEnum(IntEnum):
    MAIN = 0
    WANT_TO_ENTER = 1


class DialogueEnums:
    def __init__(self):
        self.DialogueMode = DialogueModeEnum
