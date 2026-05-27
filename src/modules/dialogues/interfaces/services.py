from abc import abstractmethod, ABC

from src.common.constants.consts import LanguageConsts
from src.common.constants.enums import LanguageEnum
from src.modules.dialogues.constants.enums import DialogueModeEnum
from src.modules.dialogues.schemas import ChatMessage, ChatBotAnswer, BotReplica


class IDialogueSrv(ABC):
    @abstractmethod
    def get_bot_answer(
        self,
        mode: DialogueModeEnum,
        messages: list[ChatMessage] = None,
        dialogue_lang: LanguageEnum | None = None,
    ) -> ChatBotAnswer:
        ...

    @abstractmethod
    def get_hello_bot_answer(
        self,
        lang: LanguageEnum = LanguageConsts.DEFAULT_LANG,
    ) -> BotReplica:
        ...

    @abstractmethod
    def get_recognized_bot_answer(
        self,
        lang: LanguageEnum = LanguageConsts.DEFAULT_LANG,
    ) -> BotReplica:
        ...

    @abstractmethod
    def get_error_bot_answer(
        self,
        lang: LanguageEnum = LanguageConsts.DEFAULT_LANG,
    ) -> BotReplica:
        ...

    @abstractmethod
    def get_want_to_enter_question_bot_answer(
        self,
        lang: LanguageEnum = LanguageConsts.DEFAULT_LANG,
    ) -> BotReplica:
        ...

    @abstractmethod
    def get_call_employee_bot_answer(
        self,
        lang: LanguageEnum = LanguageConsts.DEFAULT_LANG,
    ) -> BotReplica:
        ...

    @abstractmethod
    def get_goodbye_bot_answer(
        self,
        lang: LanguageEnum = LanguageConsts.DEFAULT_LANG,
    ) -> BotReplica:
        ...

    @abstractmethod
    def get_access_granted_bot_answer(
        self,
        lang: LanguageEnum = LanguageConsts.DEFAULT_LANG,
    ) -> BotReplica:
        ...

    @abstractmethod
    def get_access_not_granted_bot_answer(
        self,
        lang: LanguageEnum = LanguageConsts.DEFAULT_LANG,
    ) -> BotReplica:
        ...
