from abc import ABC, abstractmethod
from uuid import UUID

from src.common.schemas import PaginationResult, Pagination
from src.modules.messages.schemas import MessageInHistory


class IMessageUC(ABC):
    """
    Interface for message use case operations.

    Defines the application-level contract for message workflows.
    """

    @abstractmethod
    async def get_message_history(
        self,
        user_sid: UUID,
        visit_sid: UUID,
        pagination_params: Pagination,
    ) -> PaginationResult[MessageInHistory]:
        """
        Get message history for a visit.

        :param user_sid: Current authorized user SID.
        :param visit_sid: Visit identifier.
        :param pagination_params: Pagination params.
        :return: Visit message history.
        """
        ...
