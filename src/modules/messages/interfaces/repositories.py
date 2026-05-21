from abc import ABC, abstractmethod
from collections.abc import Sequence
from uuid import UUID

from src.common.interfaces import IPostgresBaseRepo, IS3BaseRepo
from src.common.schemas import Pagination
from src.modules.messages.models import MessageModel
from src.modules.messages.schemas import MessageCreate, MessageUpdate


class IMessagePostgresRepo(
    IPostgresBaseRepo[MessageModel, MessageCreate, MessageUpdate], ABC
):
    """
    Interface for message PostgreSQL repository operations.

    Extends base PostgreSQL repository with message-specific queries.
    """
    ...


class IMessageS3Repo(IS3BaseRepo, ABC):
    """
    Interface for a message-specific S3 repository.

    Defines additional message-related S3 operations beyond the basic S3 repository
    functionality.
    """
