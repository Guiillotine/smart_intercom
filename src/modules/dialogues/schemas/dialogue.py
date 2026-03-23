from __future__ import annotations

from src.common.schemas import CoreSchema
from src.common.constants.enums import MessageAuthorRoleEnum, LanguageEnum


class ChatMessage(CoreSchema):
    role: MessageAuthorRoleEnum
    content: str


class ChatBotAnswer(CoreSchema):
    content: str
    visitor_goal: str | None
    dialog_finished: bool
    lang: LanguageEnum
