import logging
from uuid import UUID

from fastapi import UploadFile

from src.common.constants import ErrorCodesEnums
from src.common.constants.enums import LanguageEnum
from src.common.decorators import LoggingFunctionInfo
from src.common.errors import BackendException, BotDialogueException
from src.common.interfaces import ICustomDateTime
from src.config.settings import Settings
from src.modules.dialogues.constants.enums import DialogueModeEnum
from src.modules.dialogues.interfaces import IDialogueSrv
from src.modules.dialogues.schemas.dialogue import (
    ChatMessage,
    ChatBotAnswer,
    BotReplica,
)
from src.modules.faces.interfaces import IFaceAnalyzerSrv
from src.modules.intercoms.interfaces.usecases import IIntercomUC
from src.modules.intercoms.schemas.intercom import IntercomStartedVisit, IntercomAnswer, \
    Decision, PhotoProcessingResult, IntercomAnswerWithText
from src.modules.intercoms.usecases.constants import IntercomUCEnums, IntercomUCConsts
from src.modules.messages.interfaces import IMessageSrv
from src.modules.messages.schemas import MessageVisitorCreate, MessageBotCreate, Message
from src.modules.persons.interfaces import IPersonSrv
from src.modules.speech.interfaces import ITTSSrv, IASRSrv
from src.modules.visits.constants.enums import VisitStatusEnum, VisitFinishReasonEnum, \
    VisitHandoffReasonEnum
from src.modules.visits.filters.visit import VisitFilter
from src.modules.visits.interfaces import IVisitSrv
from src.modules.visits.schemas import (
    Visit,
    VisitUpdate,
    VisitCreate,
    VisitPersonCreate,
)


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
        asr_service: IASRSrv,
        tts_service: ITTSSrv,
        visit_service: IVisitSrv,
        person_service: IPersonSrv,
        message_service: IMessageSrv,
        custom_datetime: ICustomDateTime,
        dialogue_service: IDialogueSrv,
        face_analyzer_service: IFaceAnalyzerSrv,
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
        self._person_service = person_service
        self._message_service = message_service
        self._custom_datetime = custom_datetime
        self._dialogue_service = dialogue_service
        self._face_analyzer_service = face_analyzer_service

    async def start_visit(self) -> IntercomStartedVisit:
        unfinished_visits = await self._visit_service.get_all(
            filters=VisitFilter(status=self._enums.Visit.Status.IN_PROCESS),
            requirement=self._enums.SrvReqCommon.VisitRequirements.WITH_MESSAGES,
        )

        for visit in unfinished_visits.items:
            if visit.messages:
                # TODO: author_sole == user
                await self._visit_service.finish_visit(
                    sid=visit.sid,
                    finish_reason=self._enums.Visit.FinishReason.CANCELLED_BY_VISITOR,
                )
            else:
                await self._visit_service.delete_visit(sid=visit.sid)

        visit = await self._visit_service.create_visit(
            visit_in=VisitCreate(
                status=self._enums.Visit.Status.IN_PROCESS,
                start_datetime=self._custom_datetime.get_utc_datetime(),
                dialogue_lang=self._consts.Common.DefaultLanguage,
            )
        )

        hello_bot_answer = self._dialogue_service.get_hello_bot_answer()

        intercom_answer = await self._get_intercom_answer(
            visit_sid=visit.sid,
            visit_status=visit.status,
            bot_replica=hello_bot_answer,
        )

        return IntercomStartedVisit(
            visit_sid=visit.sid,
            hello_message_audio_path=intercom_answer.answer_message_audio_path,
        )

    @LoggingFunctionInfo(description="Process visit photo.")
    async def process_visit_photo(
        self,
        visit_sid: UUID,
        photo: UploadFile,
    ) -> PhotoProcessingResult:
        await self._visit_service.save_visit_photo(sid=visit_sid, photo=photo)
        await photo.seek(0)

        photo_processing_result = PhotoProcessingResult()

        faces_info = await self._face_analyzer_service.analyse_photo(photo)

        for face in faces_info:
            visit_person_in = VisitPersonCreate(
                visit_sid=visit_sid,
                detected_age=face.detected_age,
                detected_sex=face.detected_sex,
                crop_coords=face.crop_coords,
            )

            person_sid = await self._person_service.search_by_face_embedding(
                embedding=face.face_embedding
            )
            if person_sid is not None:
                visit_person_in.person_sid = person_sid
                photo_processing_result.detected_employee = True

            await self._visit_service.create_visitor(visit_person_in)

        if photo_processing_result.detected_employee:
            created_message = await self._create_intercom_audio_and_text_message(
                visit_sid=visit_sid,
                bot_replica=self._dialogue_service.get_recognized_bot_answer(),
            )
            photo_processing_result.message_audio_path = created_message.audio_s3_path

            await self._visit_service.call_employee(
                sid=visit_sid,
                reason=self._enums.Visit.HandoffReason.EMPLOYEE_RECOGNIZED,
            )

        return photo_processing_result

    async def get_answer(
        self,
        audio: UploadFile,
        visit_sid: UUID,
    ) -> IntercomAnswerWithText:
        visit = await self._visit_service.get_by_sid(visit_sid)

        self._validate_get_answer(visit)

        speech_info = self._asr_service.speech_to_text(
            audio=audio,
            dialogue_lang=visit.dialogue_lang,
        )

        return await self.get_answer_on_text_message(
            message=speech_info.text,
            visit_sid=visit_sid,
            dialogue_lang=speech_info.lang,
        )

    async def get_answer_on_text_message(
        self,
        message: str,
        visit_sid: UUID,
        dialogue_lang: LanguageEnum | None = None,
    ) -> IntercomAnswerWithText:
        detect_language = dialogue_lang is None

        visit = await self._visit_service.get_by_sid(visit_sid)

        self._validate_get_answer(visit)

        await self._message_service.create_visitor_message(
            message_in=MessageVisitorCreate(
                visit_sid=visit_sid,
                content=message,
            ),
        )

        match visit.status:
            case self._enums.Visit.Status.IN_PROCESS:
                # State 0: Detect language
                if detect_language:
                    dialogue_lang = await self._detect_dialogue_lang_by_visitor_message(
                        message=message,
                        visit_sid=visit_sid,
                        visit_dialogue_lang=visit.dialogue_lang,
                    )
                else:
                    dialogue_lang = await self._set_visit_dialogue_lang(
                        message=message,
                        visit_sid=visit_sid,
                        visit_dialogue_lang=visit.dialogue_lang,
                        dialogue_lang=dialogue_lang,
                    )

                # State 1: Check if the visitor is calling an employee
                bot_replica, visitor_calls_employee = await (
                    self._check_visitor_call_employee(message, visit_sid, dialogue_lang)
                )

                if not visitor_calls_employee:
                    # State 2: Finding out the visitor's purpose
                    bot_replica = await self._find_out_visitor_goal(
                        visit_sid, dialogue_lang
                    )

            case self._enums.Visit.Status.ASKED_WANT_TO_ENTER:
                # State 3: Getting the visitor's answer to a 'want to enter' question
                bot_replica = await self._process_want_to_enter_visitor_answer(
                    visit_sid=visit_sid,
                    message=message,
                    dialogue_lang=visit.dialogue_lang,
                )

            # State 6: Dialogue is over
            case _:
                raise BackendException(error=self._errors.Intercom.DIALOGUE_IS_OVER)

        current_visit = await self._visit_service.get_by_sid(visit_sid)

        return await self._get_intercom_answer(
            visit_sid=visit_sid,
            visit_status=current_visit.status,
            bot_replica=bot_replica,
        )

    def _validate_get_answer(self, visit: Visit) -> None:
        if visit.status in (
            self._enums.Visit.Status.OVER,
            self._enums.Visit.Status.WAITING_DECISION
        ):
            raise BackendException(error=self._errors.Intercom.DIALOGUE_IS_OVER)

    async def _check_visitor_call_employee(
        self,
        message: str,
        visit_sid: UUID,
        dialogue_lang: LanguageEnum,
    ) -> tuple[BotReplica, bool]:
        bot_answer = await self._get_bot_answer(
            visit_sid,
            mode=self._enums.Dialogue.DialogueMode.VISITOR_CALL_EMPLOYEE,
            messages=[
                ChatMessage(
                    role=self._enums.Common.MessageAuthorRole.USER,
                    content=message,
                )
            ],
            dialogue_lang=dialogue_lang,
        )

        bot_replica = BotReplica(
            content="",
            lang=dialogue_lang,
        )

        # Transition from state 1 to state 5
        if bot_answer.call_employee:
            call_reason = self._enums.Visit.HandoffReason.VISITOR_REQUESTED_EMPLOYEE
            bot_replica = await self._call_employee(
                visit_sid, dialogue_lang, call_reason
            )

        return bot_replica, bot_answer.call_employee

    async def _detect_dialogue_lang_by_visitor_message(
        self,
        message: str,
        visit_sid: UUID,
        visit_dialogue_lang: LanguageEnum,
    ) -> LanguageEnum:
        if not self._should_change_visit_dialogue_lang(message):
          return visit_dialogue_lang

        bot_answer = await self._get_bot_answer(
            visit_sid,
            mode=self._enums.Dialogue.DialogueMode.DETECT_LANGUAGE,
            messages=[
                ChatMessage(
                    role=self._enums.Common.MessageAuthorRole.USER,
                    content=message,
                )
            ],
        )

        detected_lang = bot_answer.lang

        if visit_dialogue_lang != detected_lang:
            await self._visit_service.update_visit(
                sid=visit_sid,
                visit_in=VisitUpdate(dialogue_lang=detected_lang),
            )

        return detected_lang

    async def _set_visit_dialogue_lang(
        self,
        message: str,
        visit_sid: UUID,
        visit_dialogue_lang: LanguageEnum,
        dialogue_lang: LanguageEnum,
    ) -> LanguageEnum:
        if dialogue_lang == visit_dialogue_lang:
            return visit_dialogue_lang

        if not self._should_change_visit_dialogue_lang(message):
          return visit_dialogue_lang

        await self._visit_service.update_visit(
              sid=visit_sid,
              visit_in=VisitUpdate(dialogue_lang=dialogue_lang),
          )

        return dialogue_lang

    def _should_change_visit_dialogue_lang(
        self,
        message: str,
    ) -> bool:
        normalized_message = " ".join(message.split())

        return len(
            normalized_message
        ) >= self._settings.bot.MIN_CHARS_TO_SWITCH_DIALOGUE_LANG

    async def _find_out_visitor_goal(
        self,
        visit_sid: UUID,
        dialogue_lang: LanguageEnum,
    ) -> BotReplica:
        messages = await self._message_service.get_messages(visit_sid=visit_sid)

        chat_message_history = [ChatMessage(role=msg.role, content=msg.content) for msg in messages.items]

        bot_goal_answer = await self._get_bot_answer(
            visit_sid,
            mode=self._enums.Dialogue.DialogueMode.GOAL,
            messages=chat_message_history,
            dialogue_lang=dialogue_lang,
        )

        bot_replica_content = bot_goal_answer.content

        if bot_goal_answer.goal_identified and not bot_goal_answer.visitor_goal:
            bot_goal_answer.goal_identified = False

        if bot_goal_answer.goal_identified:
            want_to_enter_question = (
                self._dialogue_service.get_want_to_enter_question_bot_answer(
                    dialogue_lang
                ).content
            )

            bot_replica_content = bot_goal_answer.content

            # Transition from state 2 to state 3
            bot_goal_relevant_answer = await self._get_bot_answer(
                visit_sid,
                mode=self._enums.Dialogue.DialogueMode.GRANT_ACCESS,
                messages=[
                    ChatMessage(
                        role=self._enums.Common.MessageAuthorRole.USER,
                        content=bot_goal_answer.visitor_goal,
                    )
                ],
            )

            grant_access = bot_goal_relevant_answer.goal_relevant_to_company

            # Save goal info to visit for report
            await self._visit_service.update_visit(
                sid=visit_sid,
                visit_in=VisitUpdate(
                    visitor_goal=bot_goal_answer.visitor_goal,
                    bot_granted_access=grant_access,
                )
            )

            # Transition from state 3 to state 5
            if grant_access:
                call_reason=self._enums.Visit.HandoffReason.READY_FOR_EMPLOYEE_DECISION
                bot_call_employee_replica = await self._call_employee(
                    visit_sid, dialogue_lang, call_reason
                )
                bot_replica_content = f"{bot_replica_content} {bot_call_employee_replica.content}"

            # Transition from state 3 to state 4
            else:
                await self._visit_service.ask_want_to_enter(visit_sid)
                bot_replica_content = f"{bot_replica_content} {want_to_enter_question}"

        return BotReplica(
            content=bot_replica_content,
            lang=dialogue_lang,
        )

    async def _process_want_to_enter_visitor_answer(
        self,
        message: str,
        visit_sid: UUID,
        dialogue_lang: LanguageEnum,
    ) -> BotReplica:
        messages = [
            ChatMessage(role=self._enums.Common.MessageAuthorRole.USER, content=message)
        ]

        bot_answer = await self._get_bot_answer(
            visit_sid,
            mode=self._enums.Dialogue.DialogueMode.WANT_TO_ENTER,
            messages=messages,
        )

        if bot_answer.want_to_enter:
            call_reason=self._enums.Visit.HandoffReason.READY_FOR_EMPLOYEE_DECISION
            bot_replica = await self._call_employee(
                visit_sid, dialogue_lang, call_reason
            )

        else:
            finish_reason = self._enums.Visit.FinishReason.CANCELLED_BY_VISITOR
            bot_replica = await self._finish_visit(
                visit_sid, dialogue_lang, finish_reason
            )

        return bot_replica

    async def _get_bot_answer(
        self,
        visit_sid: UUID,
        mode: DialogueModeEnum,
        messages: list[ChatMessage] | None = None,
        dialogue_lang: LanguageEnum | None = None,
    ) -> ChatBotAnswer:
        if messages is None:
          messages = []

        try:
            bot_answer = self._dialogue_service.get_bot_answer(
              mode=mode,
              messages=messages,
              dialogue_lang=dialogue_lang,
            )
            self._logger.debug(f"Bot answer: {bot_answer}")

        except Exception as e:
            self._logger.exception(e)

            await self._visit_service.call_employee(
                sid=visit_sid,
                reason=self._enums.Visit.HandoffReason.BOT_ERROR,
            )

            # Save bot error message
            message = await self._create_intercom_audio_and_text_message(
                visit_sid=visit_sid,
                bot_replica=self._dialogue_service.get_error_bot_answer(
                    lang=dialogue_lang or self._consts.Common.DefaultLanguage
                )
            )
            if isinstance(e, BackendException):
                raise BotDialogueException.from_backend_exception(
                    exc=e, audio_s3_path=message.audio_s3_path,
                ) from e

            raise BotDialogueException(
                error=self._errors.Common.UNDEFINED,
                audio_s3_path=message.audio_s3_path,
            ) from e

        return bot_answer

    async def _get_intercom_answer(
        self,
        visit_sid: UUID,
        visit_status: VisitStatusEnum,
        bot_replica: BotReplica,
    ) -> IntercomAnswerWithText:
        try:
            created_message = await self._create_intercom_audio_and_text_message(
                visit_sid, bot_replica,
            )

            dialogue_finished = (
                visit_status in (
                    self._enums.Visit.Status.OVER,
                    self._enums.Visit.Status.WAITING_DECISION,
                )
            )

            return IntercomAnswerWithText(
                answer_message_audio_path=created_message.audio_s3_path,
                dialogue_finished=dialogue_finished,
                answer_message_text=created_message.content,
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

        bot_replica = self._dialogue_service.get_error_bot_answer()

        created_message = await self._create_intercom_audio_and_text_message(
            visit_sid, bot_replica,
        )

        return IntercomAnswer(
            answer_message_audio_path=created_message.audio_s3_path,
        )

    @LoggingFunctionInfo(description="Get user door opening decision for visit.")
    async def get_user_decision(self, visit_sid: UUID) -> Decision:
        visit = await self._visit_service.get_by_sid(visit_sid)
        return Decision(open=visit.granted_access)

    async def _create_intercom_audio_and_text_message(
        self,
        visit_sid: UUID,
        bot_replica: BotReplica,
    ) -> Message:
        audio_data = self._tts_service.synthesize(
            text=bot_replica.content, lang=bot_replica.lang,
        )

        return await self._message_service.create_bot_message(
            message_in=MessageBotCreate(
                audio=audio_data.data,
                content=bot_replica.content,
                visit_sid=visit_sid,
            )
        )

    async def _call_employee(
        self,
        visit_sid: UUID,
        dialogue_lang: LanguageEnum,
        call_reason: VisitHandoffReasonEnum,
    ) -> BotReplica:
        bot_replica = self._dialogue_service.get_call_employee_bot_answer(
            lang=dialogue_lang
        )

        await self._visit_service.call_employee(
            visit_sid, reason=call_reason,
        )

        return bot_replica

    async def _finish_visit(
        self,
        visit_sid: UUID,
        dialogue_lang: LanguageEnum,
        finish_reason: VisitFinishReasonEnum,
    ) -> BotReplica:
        bot_replica = self._dialogue_service.get_goodbye_bot_answer(
            lang=dialogue_lang
        )

        await self._visit_service.finish_visit(
            sid=visit_sid, finish_reason=finish_reason,
        )

        return bot_replica
