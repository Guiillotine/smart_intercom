from enum import StrEnum


class MessageAuthorRoleEnum(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class MessageEnums:
    def __init__(self):
        self.MessageAuthorRole = MessageAuthorRoleEnum
