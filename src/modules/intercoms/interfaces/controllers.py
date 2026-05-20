from abc import ABC, abstractmethod
from uuid import UUID

from fastapi import APIRouter, UploadFile

from src.common.constants.enums import LanguageEnum
from src.common.schemas import Msg
from src.modules.intercoms.interfaces.usecases import IIntercomUC
from src.modules.intercoms.schemas import Decision, IntercomAnswer, IntercomStartedVisit


class IIntercomController(ABC):
    """
    Interface for intercom controller operations.

    Defines the contract for all intercom-related API endpoints.
    """

    @property
    @abstractmethod
    def controller(self) -> APIRouter:
        """
        Get the configured APIRouter instance.

        :return: Configured FastAPI router with intercom routes.
        """
        ...

    @staticmethod
    @abstractmethod
    async def start_visit(intercom_usecase: IIntercomUC) -> IntercomStartedVisit:
        """
        Start a new intercom visit.

        :param intercom_usecase: Intercom use case dependency.
        :return: Started visit data.
        """
        ...

    @staticmethod
    @abstractmethod
    async def process_visit_photo(
        visit_sid: UUID,
        photo: UploadFile,
        intercom_usecase: IIntercomUC,
    ) -> Msg:
        """
        Process visit photo.

        :param visit_sid: Visit identifier.
        :param photo: Uploaded photo file.
        :param intercom_usecase: Intercom use case dependency.
        :return: Operation result message.
        """
        ...

    @staticmethod
    @abstractmethod
    async def get_answer(
        visit_sid: UUID,
        audio: UploadFile,
        intercom_usecase: IIntercomUC,
    ) -> IntercomAnswer:
        """
        Get intercom answer for uploaded audio.

        :param visit_sid: Visit identifier.
        :param audio: Uploaded audio file.
        :param intercom_usecase: Intercom use case dependency.
        :return: Intercom answer data.
        """
        ...

    @staticmethod
    @abstractmethod
    async def get_answer_on_text_message(
        visit_sid: UUID,
        message: str,
        intercom_usecase: IIntercomUC,
    ) -> IntercomAnswer:
        """
        Get intercom answer for text message.

        :param visit_sid: Visit identifier.
        :param message: Visitor text message.
        :param intercom_usecase: Intercom use case dependency.
        :return: Intercom answer data.
        """
        ...

    @staticmethod
    @abstractmethod
    async def get_user_decision(
        visit_sid: UUID,
        intercom_usecase: IIntercomUC,
    ) -> Decision:
        """
        Get user door opening decision for visit.

        :param visit_sid: Visit identifier.
        :param intercom_usecase: Intercom use case dependency.
        :return: Decision data.
        """
        ...
