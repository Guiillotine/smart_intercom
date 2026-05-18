from __future__ import annotations

from src.common.schemas import CoreSchema
from src.common.constants.enums import MessageAuthorRoleEnum, LanguageEnum


class ChatMessage(CoreSchema):
    role: MessageAuthorRole
    content: str


class ChatBotAnswerBase(CoreSchema):
    """What LLM answered"""
    pass


class BotReplica(ChatBotAnswerBase):
    """What will be announced to the visitor"""
    content: str
    lang: LanguageEnum
    error: bool = False


class DetectLanguageBotAnswer(ChatBotAnswerBase):
    lang: LanguageEnum


class GoalDialogBotAnswer(ChatBotAnswerBase):
    content: str
    visitor_goal: str | None = None
    goal_identified: bool = False


class GrantAccessDialogBotAnswer(CoreSchema):
    goal_relevant_to_company: bool = False


class VisitorCallEmployeeBotAnswer(ChatBotAnswerBase):
    call_employee: bool = False


class WantToEnterBotAnswer(ChatBotAnswerBase):
    want_to_enter: bool


ChatBotAnswer = DetectLanguageBotAnswer | VisitorCallEmployeeBotAnswer | GrantAccessDialogBotAnswer | GoalDialogBotAnswer | GrantAccessDialogBotAnswer | WantToEnterBotAnswer


class DialogConfig(CoreSchema):
    initial_prompt: str
    bot_answer_schema_prompt: str
    bot_answer_schema: type[CoreSchema]
