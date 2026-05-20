from abc import ABC, abstractmethod
from uuid import UUID

from src.modules.messages.schemas import (
    Message,
    MessageBotCreate,
    MessageInHistory,
    MessageVisitorCreate,
)


class IMessageSrv(ABC):
    """
    Interface for message service operations.

    Defines business operations for creating and reading visit messages.
    """

    @abstractmethod
    async def create_visitor_message(
        self, message_in: MessageVisitorCreate
    ) -> Message:
        """
        Create a visitor message.

        :param message_in: Visitor message creation schema.
        :return: Created message.
        """
        ...

    @abstractmethod
    async def create_bot_message(self, message_in: MessageBotCreate) -> Message:
        """
        Create a bot message.

        :param message_in: Bot message creation schema.
        :return: Created message.
        """
        ...

    @abstractmethod
    async def get_messages(self, visit_sid: UUID) -> list[Message]:
        """
        Get full message models for a visit.

        :param visit_sid: Visit identifier.
        :return: List of messages.
        """
        ...

    @abstractmethod
    async def get_message_history(self, visit_sid: UUID) -> list[MessageInHistory]:
        """
        Get public message history for a visit.

        :param visit_sid: Visit identifier.
        :return: Message history list.
        """
        ...
