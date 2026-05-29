from abc import ABC, abstractmethod
from uuid import UUID

from fastapi import UploadFile

from src.common.constants.enums import LanguageEnum
from src.common.schemas import Msg
from src.modules.intercoms.schemas import Decision, IntercomAnswer, \
    IntercomStartedVisit, PhotoProcessingResult, IntercomAnswerWithText


class IIntercomUC(ABC):
    """
    Interface for intercom use case operations.

    Defines application-level intercom workflows.
    """

    @abstractmethod
    async def start_visit(self) -> IntercomStartedVisit:
        """
        Start a new intercom visit.

        :return: Started visit data.
        """
        ...

    @abstractmethod
    async def process_visit_photo(
        self,
        visit_sid: UUID,
        photo: UploadFile,
    ) -> PhotoProcessingResult:
        """
        Process visit photo.

        :param visit_sid: Visit identifier.
        :param photo: Uploaded photo file.
        :return: Operation result message.
        """
        ...

    @abstractmethod
    async def get_answer(
        self,
        audio: UploadFile,
        visit_sid: UUID,
    ) -> IntercomAnswer:
        """
        Get intercom answer for uploaded audio.

        :param audio: Uploaded audio file.
        :param visit_sid: Visit identifier.
        :return: Intercom answer data.
        """
        ...

    @abstractmethod
    async def get_answer_on_text_message(
        self,
        message: str,
        visit_sid: UUID,
        dialogue_lang: LanguageEnum | None = None,
    ) -> IntercomAnswerWithText:
        """
        Get intercom answer for text message.

        :param message: Visitor text message.
        :param visit_sid: Visit identifier.
        :param dialogue_lang: Optional dialogue language.
        :return: Intercom answer data.
        """
        ...

    @abstractmethod
    async def get_user_decision(self, visit_sid: UUID) -> Decision:
        """
        Get user door opening decision for visit.

        :param visit_sid: Visit identifier.
        :return: Decision data.
        """
        ...
