from abc import ABC, abstractmethod
from collections.abc import Sequence
from uuid import UUID

from src.common.interfaces import IPostgresBaseRepo
from src.modules.messages.models import MessageModel
from src.modules.messages.schemas import MessageCreate, MessageUpdate


class IMessagePostgresRepo(
    IPostgresBaseRepo[MessageModel, MessageCreate, MessageUpdate], ABC
):
    """
    Interface for message PostgreSQL repository operations.

    Extends base PostgreSQL repository with message-specific queries.
    """

    @abstractmethod
    async def get_by_visit_sid(self, visit_sid: UUID) -> Sequence[MessageModel]:
        """
        Get all messages for a visit.

        :param visit_sid: Visit identifier.
        :return: Sequence of message database models.
        """
        ...
