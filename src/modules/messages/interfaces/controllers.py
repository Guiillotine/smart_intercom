from abc import ABC, abstractmethod
from uuid import UUID

from fastapi import APIRouter

from src.common.schemas import Pagination, PaginationResult
from src.modules.messages.interfaces.usecases import IMessageUC
from src.modules.messages.schemas import MessageInHistory


class IMessageCtrl(ABC):
    """
    Interface for message controller operations.

    Defines the contract for all message-related API endpoints.
    """

    @property
    @abstractmethod
    def controller(self) -> APIRouter:
        """
        Get the configured APIRouter instance.

        :return: Configured FastAPI router with all message routes.
        """
        ...

    @staticmethod
    @abstractmethod
    async def get_visit_message_history(
        user_sid: UUID,
        visit_sid: UUID,
        pagination_params: Pagination,
        message_usecase: IMessageUC,
    ) -> PaginationResult[MessageInHistory]:
        """
        Get message history for a visit.

        :param user_sid: Current authorized user SID.
        :param visit_sid: Visit identifier.
        :param message_usecase: Message use case dependency.
        :param pagination_params: Pagination params.
        :return: List of messages ordered by creation time.
        """
        ...
