from src.common.constants.enums import MessageAuthorRoleEnum, LanguageEnum
from src.common.schemas import CoreSchema


class ChatMessage(CoreSchema):
    role: MessageAuthorRoleEnum
    content: str


class ChatBotAnswerBase(CoreSchema):
    """What LLM answered"""
    pass


class BotReplica(ChatBotAnswerBase):
    """What will be announced to the visitor"""
    content: str
    lang: LanguageEnum


class DetectLanguageBotAnswer(ChatBotAnswerBase):
    lang: LanguageEnum


class GoalDialogueBotAnswer(ChatBotAnswerBase):
    content: str
    visitor_goal: str | None = None
    goal_identified: bool = False


class GrantAccessDialogueBotAnswer(CoreSchema):
    goal_relevant_to_company: bool = False


class VisitorCallEmployeeBotAnswer(ChatBotAnswerBase):
    call_employee: bool = False


class WantToEnterBotAnswer(ChatBotAnswerBase):
    want_to_enter: bool


ChatBotAnswer = DetectLanguageBotAnswer | VisitorCallEmployeeBotAnswer | GrantAccessDialogueBotAnswer | GoalDialogueBotAnswer | WantToEnterBotAnswer


class DialogueConfig(CoreSchema):
    initial_prompt: str
    bot_answer_schema_prompt: str
    bot_answer_schema: type[CoreSchema]
