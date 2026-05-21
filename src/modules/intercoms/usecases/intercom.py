import logging
from uuid import UUID

from fastapi import UploadFile

from src.common.constants import ErrorCodesEnums
from src.common.constants.enums import LanguageEnum
from src.common.decorators import LoggingFunctionInfo
from src.common.errors import BackendException
from src.common.schemas import Msg
from src.config.settings import Settings
from src.modules.dialogues.constants.enums import DialogueModeEnum
from src.modules.dialogues.schemas.dialogue import (
    ChatMessage,
    ChatBotAnswer,
    BotReplica,
)
from src.modules.intercoms.interfaces.usecases import IIntercomUC
from src.modules.intercoms.schemas.intercom import IntercomStartedVisit, IntercomAnswer, \
    Decision
from src.modules.intercoms.usecases.constants import IntercomUCEnums, IntercomUCConsts
from src.modules.messages.interfaces import IMessageSrv
from src.modules.messages.schemas import MessageVisitorCreate, MessageBotCreate
from src.modules.speech.interfaces import ITTSService
from src.modules.visits.constants.enums import VisitStatusEnum
from src.modules.visits.interfaces import IVisitSrv
from src.modules.visits.schemas import Visit, VisitCallEmployee, VisitFinish, \
    VisitUpdateShort, VisitUpdate


class IntercomUC(IIntercomUC):
    """
    Use case layer for intercom data retrieval, delegating calls to the intercom
    service.
    """

    def __init__(
        self,
        enums: IntercomUCEnums,
        consts: IntercomUCConsts,
        logger: logging.Logger,
        errors: ErrorCodesEnums,
        settings: Settings,
        asr_service: IASRService,
        tts_service: ITTSService,
        visit_service: IVisitSrv,
        dialog_service: IDialogSrv,
        message_service: IMessageSrv,
    ):
        """
        Initialize the IntercomUC.
        """
        self._enums = enums
        self._consts = consts
        self._errors = errors
        self._logger = logger
        self._settings = settings
        self._asr_service = asr_service
        self._tts_service = tts_service
        self._visit_service = visit_service
        self._dialog_service = dialog_service
        self._message_service = message_service

    async def start_visit(self) -> IntercomStartedVisit:
        # TODO:
        # 1. Get all unfinished visits
        # 2. Delete unfinished visits without data (no user messages) + s3

        visit = await self._visit_service.create_visit()

        hello_bot_answer = self._dialog_service.get_hello_bot_answer()

        intercom_answer = await self._get_intercom_answer(
            visit_sid=visit.sid,
            visit_status=visit.status,
            bot_replica=hello_bot_answer,
        )

        return IntercomStartedVisit(
            visit_sid = visit.sid,
            hello_message_audio_path = intercom_answer.answer_message_audio_path,
        )

    @LoggingFunctionInfo(description="Process visit photo.")
    async def process_visit_photo(self, visit_sid: UUID, photo: UploadFile) -> Msg:
        # TODO:
        # 1. Process photo
        # 2. Identification by embedding (Person table)
        # 3. Call user if employee was detected
        ...

    async def get_answer(
        self,
        audio: UploadFile,
        visit_sid: UUID,
    ) -> IntercomAnswer:
         # TODO: get visit, get dialog_lang

        speech_info = await self._asr_service.speech_to_text(
            audio=audio,
        )

        return await self.get_answer_on_text_message(
            message=speech_info.text,
            visit_sid=visit_sid,
            dialog_lang=speech_info.lang,
        )

    async def get_answer_on_text_message(
        self,
        message: str,
        visit_sid: UUID,
        dialog_lang: LanguageEnum | None = None,
    ) -> IntercomAnswer:
        detect_language = dialog_lang is not None

        visit = await self._visit_service.get_by_sid(visit_sid)

        self._validate_get_answer(visit)

        await self._message_service.create_visitor_message(
            message_in=MessageVisitorCreate(
                visit_sid=visit_sid,
                content=message,
            ),
        )

        bot_replica: BotReplica | None = None

        match visit.status:
            case self._enums.Visit.VisitStatus.IN_PROCESS:
                # State 0: Detect language
                if detect_language:
                    dialog_lang = await self._detect_dialog_lang_by_visitor_message(
                        message=message,
                        visit_sid=visit_sid,
                        visit_dialog_lang=visit.dialog_lang,
                    )
                else:
                    dialog_lang = await self._set_visit_dialog_lang(
                        message=message,
                        visit_sid=visit_sid,
                        visit_dialog_lang=visit.dialog_lang,
                        dialog_lang=dialog_lang,
                    )

                # State 1: Check if the visitor is calling an employee
                bot_replica, visitor_calls_employee = await (
                    self._check_visitor_call_employee(message, visit_sid, dialog_lang)
                )

                if not visitor_calls_employee:
                    # State 2: Finding out the visitor's purpose
                    bot_replica = await self._find_out_visitor_goal(
                        visit_sid, dialog_lang
                    )

            case self._enums.Visit.VisitStatus.ASKED_WANT_TO_ENTER:
                # State 3: Getting the visitor's answer to a 'want to enter' question
                bot_replica = await self._process_want_to_enter_visitor_answer(
                    visit_sid=visit_sid,
                    message=message,
                    visitor_goal=visit.visitor_goal,
                    bot_granted_access=visit.bot_granted_access,
                    dialog_lang=visit.dialog_lang,
                )

            # State 6: Dialog is over
            case _:
                raise BackendException(error=self._errors.Intercom.DIALOG_IS_OVER)

        current_visit = await self._visit_service.get_by_sid(visit_sid)

        return await self._get_intercom_answer(
            visit_sid=visit_sid,
            visit_status=current_visit.status,
            bot_replica=bot_replica,
        )

    def _validate_get_answer(self, visit: Visit) -> None:
        if visit.status in (
            self._enums.Visit.VisitStatus.OVER,
            self._enums.Visit.VisitStatus.WAITING_DECISION
        ):
            raise BackendException(error=self._errors.Intercom.DIALOG_IS_OVER)

    async def _check_visitor_call_employee(
        self,
        message: str,
        visit_sid: UUID,
        dialog_lang: LanguageEnum,
    ) -> tuple[BotReplica, bool]:
        bot_answer = await self._get_bot_answer(
            visit_sid,
            mode=self._enums.Dialogue.DialogueMode.VISITOR_CALL_EMPLOYEE,
            messages=[ChatMessage(role=self._enums.Common.MessageAuthorRole.USER, content=message)],
            dialog_lang=dialog_lang,
        )

        if bot_answer.error: # TODO: to BotReplica !
            return (bot_answer, True)

        bot_replica = BotReplica(
            content="",
            lang=dialog_lang,
        )

        if bot_answer.call_employee:
            bot_replica.content = await (
                self._dialog_service.get_call_employee_bot_answer(lang=dialog_lang)
            ).content

            # Transition from state 1 to state 5
            await self._visit_service.call_employee(sid=visit_sid)

        return bot_replica, bot_answer.call_employee

    async def _detect_dialog_lang_by_visitor_message(
        self,
        message: str,
        visit_sid: UUID,
        visit_dialog_lang: LanguageEnum,
    ) -> LanguageEnum:
        if not self._should_change_visit_dialog_lang(message):
          return visit_dialog_lang

        bot_answer = await self._get_bot_answer(
            visit_sid,
            mode=self._enums.Dialogue.DialogueMode.DETECT_LANGUAGE,
            messages=[
                ChatMessage(role=self._enums.Common.MessageAuthor.USER, content=message)
            ],
        )

        if bot_answer.error:  # TODO: to BotReplica !
            print("Can't detect message language")
            return self._enums.Common.Language.RU

        delected_lang = bot_answer.lang

        if visit_dialog_lang != delected_lang:
            await self._visit_service.update_visit(
                sid=visit_sid,
                visit_in=VisitUpdate.model_validate(
                    VisitUpdateShort(dialog_lang=delected_lang)
                ),
            )

        return delected_lang

    async def _set_visit_dialog_lang (
        self,
        message: str,
        visit_sid: UUID,
        visit_dialog_lang: LanguageEnum,
        dialog_lang: LanguageEnum,
    ) -> LanguageEnum:
        if dialog_lang == visit_dialog_lang:
            return visit_dialog_lang

        if not self._should_change_visit_dialog_lang(message):
          return visit_dialog_lang

        await self._visit_service.update_visit(
              sid=visit_sid,
              visit_in=VisitUpdate.model_validate(
                  VisitUpdateShort(dialog_lang=dialog_lang)
              ),
          )

        return dialog_lang

    def _should_change_visit_dialog_lang(
        self,
        message: str,
    ) -> bool:
        normalized_message = " ".join(message.split())

        return len(
            normalized_message
        ) >= self._settings.bot.MIN_CHARS_TO_SWITCH_DIALOG_LANG

    async def _find_out_visitor_goal(
        self,
        visit_sid: UUID,
        dialog_lang: LanguageEnum,
    ) -> BotReplica:
        messages = await self._message_service.get_messages(visit_sid=visit_sid)

        chat_message_history = [ChatMessage(role=msg.role, content=msg.content) for msg in messages]

        bot_goal_answer = await self._get_bot_answer(
            visit_sid,
            mode=self._enums.Dialogue.DialogueMode.GOAL,
            messages=chat_message_history,
            dialog_lang=dialog_lang,
        )

        if bot_goal_answer.error:  # TODO: to BotReplica !
            return bot_goal_answer

        bot_replica_content = bot_goal_answer.content

        if bot_goal_answer.goal_identified:
            want_to_enter_question = self._dialog_service.get_want_to_enter_question_bot_answer(dialog_lang).content

            bot_replica_content = f"{bot_goal_answer.content} {want_to_enter_question}"

            # Transition from state 2 to state 3
            bot_goal_relevant_answer = await self._get_bot_answer(
                visit_sid,
                mode=self._enums.Dialogue.DialogueMode.GRANT_ACCESS,
                messages=[
                    ChatMessage(
                        role=self._enums.Message.MessageAuthorRole.USER,
                        content=bot_goal_answer.visitor_goal,
                    )
                ],
            )

            if bot_goal_relevant_answer.error:  # TODO: to BotReplica !
                return bot_goal_relevant_answer

            grant_access = bot_goal_relevant_answer.goal_relevant_to_company

            # Transition from state 3 to state 4
            await self._visit_service.ask_want_to_enter(
                sid=visit_sid,
                visitor_goal=bot_goal_answer.visitor_goal,
                bot_granted_access=grant_access,
            )

        return BotReplica(
            content=bot_replica_content,
            lang=dialog_lang,
        )

    async def _process_want_to_enter_visitor_answer(
        self,
        message: str,
        visit_sid: UUID,
        visitor_goal: str,
        bot_granted_access: bool,
        dialog_lang: LanguageEnum,
    ) -> BotReplica:
        # TODO
        messages = [ChatMessage(role=self._enums.Message.MessageAuthorRole.USER, content=message)]

        bot_answer = await self._get_bot_answer(
            visit_sid,
            mode=self._enums.Dialogue.DialogueMode.WANT_TO_ENTER,
            messages=messages,
            visitor_goal=visitor_goal,
            bot_granted_access=bot_granted_access,
        )

        if bot_answer.error:  # TODO: to BotReplica !
            return bot_answer

        if bot_answer.want_to_enter:
            bot_replica = self._dialog_service.get_call_employee_bot_answer(lang=dialog_lang)

            await self._visit_service.call_employee(
              visit_sid,
              visit_call_employee_params=VisitCallEmployee(
                  visitor_goal=visitor_goal,
                  bot_granted_access=bot_granted_access,
              ),
          )

        else:
            bot_replica = self._dialog_service.get_goodbye_bot_answer(lang=dialog_lang)

            await self._visit_service.finish_visit(
                visit_sid,
                visit_finish_params=VisitFinish(
                    finish_reason=self._enums.Visit.VisitFinishReason.CANCELLED_BY_VISITOR,
                    visitor_goal=visitor_goal,
                    bot_granted_access=bot_granted_access,
                ),
            )

        return bot_replica

    async def _get_bot_answer(
        self,
        visit_sid: UUID,
        mode: DialogueModeEnum,
        messages: list[ChatMessage] = None,
        visitor_goal: str | None = None,
        bot_granted_access: bool | None = None,
        dialog_lang: LanguageEnum | None = None,
    ) -> ChatBotAnswer:
        if messages is None:
          messages = []

        try:
            bot_answer = await self._dialog_service.get_bot_answer(
              mode=mode,
              messages=messages,
              dialog_lang=dialog_lang,
            )

            print("\n\n BOT ANSWER:", bot_answer)

        except Exception as e:
            visit_call_employee_params=VisitCallEmployee(
                finish_reason=self._enums.Visit.VisitFinishReason.BOT_ERROR,
            )

            if visitor_goal is not None:
                visit_call_employee_params.visitor_goal=visitor_goal

            if bot_granted_access is not None:
                visit_call_employee_params.bot_granted_access=bot_granted_access

            await self._visit_service.call_employee(
                sid=visit_sid,
                visit_call_employee_params=visit_call_employee_params,
            )

            return self._dialog_service.get_error_bot_answer(
                lang=dialog_lang or self._consts.Common.DefaultLanguage
            )

        return bot_answer

    async def _get_intercom_answer(
        self,
        visit_sid: UUID,
        visit_status: VisitStatusEnum,
        bot_replica: BotReplica,
    ) -> IntercomAnswer:
        try:
            audio_data = await self._tts_service.synthesize(
                text=bot_replica.content, lang=bot_replica.lang,
            )

            created_message = await self._message_service.create_bot_message(
                message_in=MessageBotCreate(
                    audio=audio_data.audio,
                    content=bot_replica.content,
                    visit_sid=visit_sid,
                )
            )

            dialog_finished = (
                visit_status == self._enums.Visit.VisitStatus.WAITING_DECISION
            )

            return IntercomAnswer(
                answer_message_audio_path=created_message.audio_s3_path,
                dialog_finished=dialog_finished,
            )

        except Exception as e:
            return await self._get_fallback_intercom_answer(visit_sid)

    async def _get_fallback_intercom_answer(
        self,
        visit_sid: UUID,
    ) -> IntercomAnswer:
        """
        For errors where the bot-defined language and the actual language are inconsistent
        """

        bot_replica = self._dialog_service.get_error_bot_answer()

        audio_data = await self._tts_service.synthesize(
            text=bot_replica.content, lang=bot_replica.lang,
        )

        created_message = await self._message_service.create_bot_message(
            message_in=MessageBotCreate(
                audio=audio_data.audio,
                content=bot_replica.content,
                visit_sid=visit_sid,
            )
        )

        return IntercomAnswer(
            answer_message_audio_path=created_message.audio_s3_path,
        )

    @LoggingFunctionInfo(description="Get user door opening decision for visit.")
    async def get_user_decision(self, visit_sid: UUID) -> Decision:
        ...
