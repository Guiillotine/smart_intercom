import logging
from time import perf_counter

import openai
from openai import OpenAI
from pydantic import ValidationError

from src.common.constants import ErrorCodesEnums
from src.common.constants.consts import LanguageConsts
from src.common.constants.enums import LanguageEnum
from src.common.errors import BackendException
from src.common.schemas import CoreSchema
from src.config.settings import Settings
from src.modules.dialogues.constants import DialogueEnums, DialogueConsts
from src.modules.dialogues.constants.enums import DialogueModeEnum
from src.modules.dialogues.interfaces import IDialogueSrv
from src.modules.dialogues.schemas import ChatMessage, ChatBotAnswer, BotReplica, \
    ChatBotAnswerBase


class DialogueSrv(IDialogueSrv):
    def __init__(
        self,
        logger: logging.Logger,
        enums: DialogueEnums,
        consts: DialogueConsts,
        errors: ErrorCodesEnums,
        settings: Settings,
        client: OpenAI,
    ):
        self._logger = logger
        self._enums = enums
        self._consts = consts
        self._errors = errors
        self._settings = settings
        self._client = client

    def get_bot_answer(
        self,
        mode: DialogueModeEnum,
        messages: list[ChatMessage] = None,
        dialogue_lang: LanguageEnum | None = None,
    ) -> ChatBotAnswer:
        if messages is None:
            messages = []

        config = self._consts.DialogueConfig.MODE_CONFIG_MAP.get(mode)

        initial_system_message = ChatMessage(
            role=self._enums.Common.MessageAuthorRole.SYSTEM,
            content=config.initial_prompt,
        )

        if not self._settings.bot.MODEL_SUPPORTS_STRUCTURED_OUTPUTS:
            initial_system_message.content += ("\n\n" + config.bot_answer_schema_prompt)

        message_history: list[ChatMessage] = [initial_system_message]

        if dialogue_lang is not None:
            message_history.append(
                ChatMessage(
                    role=self._enums.Common.MessageAuthorRole.SYSTEM,
                    content=self._consts.Prompt.DIALOGUE_LANGUAGE_PROMPT.format(
                        dialogue_lang.value
                    )
                )
            )

        message_history += messages

        for attempt in range(0, self._settings.bot.LLM_INVALID_JSON_RETRIES + 1):
            try:
                llm_started_at = perf_counter()
                completion = self._send_to_llm(
                    messages=message_history,
                    bot_answer_schema=config.bot_answer_schema,
                )
                self._logger.info(
                    "[PERF] llm_http_request_ms=%.2f mode=%s attempt=%d",
                    self._elapsed_ms(llm_started_at),
                    mode,
                    attempt + 1,
                )

                self._logger.debug("SENT TO LLM:")
                for num, msg in enumerate(message_history):
                    self._logger.debug(f"{num} -> {msg}")

                raw_content = completion.choices[0].message.content

                parsed_answer = config.bot_answer_schema.model_validate_json(
                    raw_content
                )

                return parsed_answer

            except ValidationError:
                self._logger.warning("Model returned an invalid json.")
                continue

            except openai.BadRequestError as e:
                self._logger.exception(e)
                raise BackendException(error=self._errors.Dialogue.BAD_REQUEST)

            except openai.RateLimitError as e:
                self._logger.exception(e)
                raise BackendException(error=self._errors.Dialogue.RATE_LIMIT_ERROR)

            except openai.InternalServerError as e:
                self._logger.exception(e)
                raise BackendException(error=self._errors.Dialogue.OPENAI)

            except openai.APITimeoutError as e:
                self._logger.exception(e)
                raise BackendException(error=self._errors.Dialogue.WAITING_DECISION_TIMEOUT)

            except Exception as e:
                self._logger.exception(e)
                raise BackendException(error=self._errors.Common.UNDEFINED)

        raise BackendException(error=self._errors.Dialogue.INVALID_LLM_RESPONSE)

    def get_hello_bot_answer(
        self,
        lang: LanguageEnum = LanguageConsts.DEFAULT_LANG,
    ) -> BotReplica:
        lang = LanguageConsts.DEFAULT_LANG
        return BotReplica(
            content=self._consts.Message.get(self._enums.BotMessage.HELLO, lang),
            lang=lang,
        )

    def get_recognized_bot_answer(
        self,
        lang: LanguageEnum = LanguageConsts.DEFAULT_LANG,
    ) -> BotReplica:
        return BotReplica(
            content=self._consts.Message.get(self._enums.BotMessage.RECOGNIZED, lang),
            lang=lang,
        )

    def get_error_bot_answer(
        self,
        lang: LanguageEnum = LanguageConsts.DEFAULT_LANG,
    ) -> BotReplica:
        return BotReplica(
            content=self._consts.Message.get(self._enums.BotMessage.ERROR, lang),
            lang=lang,
            error=True,
        )

    def get_want_to_enter_question_bot_answer(self, lang: LanguageEnum = LanguageConsts.DEFAULT_LANG) -> BotReplica:
        return BotReplica(
            content=self._consts.Message.get(self._enums.BotMessage.WANT_TO_ENTER_QUESTION, lang),
            lang=lang,
        )

    def get_call_employee_bot_answer(self, lang: LanguageEnum = LanguageConsts.DEFAULT_LANG) -> BotReplica:
        return BotReplica(
            content=self._consts.Message.get(self._enums.BotMessage.CALL_EMPLOYEE, lang),
            lang=lang,
        )

    def get_goodbye_bot_answer(self, lang: LanguageEnum = LanguageConsts.DEFAULT_LANG) -> BotReplica:
        return BotReplica(
            content=self._consts.Message.get(self._enums.BotMessage.GOODBYE, lang),
            lang=lang,
        )

    def get_access_granted_bot_answer(self, lang: LanguageEnum = LanguageConsts.DEFAULT_LANG) -> BotReplica:
        return BotReplica(
            content=self._consts.Message.get(self._enums.BotMessage.ACCESS_GRANTED, lang),
            lang=lang,
        )

    def get_access_not_granted_bot_answer(self, lang: LanguageEnum = LanguageConsts.DEFAULT_LANG) -> BotReplica:
        return BotReplica(
            content=self._consts.Message.get(self._enums.BotMessage.ACCESS_NOT_GRANTED, lang),
            lang=lang,
        )

    def _send_to_llm(
        self,
        messages: list[ChatMessage],
        bot_answer_schema: type[ChatBotAnswerBase],
    ):
        if self._settings.bot.MODEL_SUPPORTS_STRUCTURED_OUTPUTS:
            response_format = {
                "type": "json_schema",
                "json_schema": {
                    "name": "chat_bot_answer",
                    "schema": bot_answer_schema.model_json_schema(),
                    "strict": True,
                },
            }
        else:
            response_format = {"type": "json_object"}

        return self._client.chat.completions.create(
            model=self._settings.bot.MODEL,
            messages=[message.model_dump() for message in messages],
            temperature=0.2,
            n=1,
            max_tokens=200,
            response_format=response_format,
        )

    @staticmethod
    def _elapsed_ms(started_at: float) -> float:
        return (perf_counter() - started_at) * 1000
