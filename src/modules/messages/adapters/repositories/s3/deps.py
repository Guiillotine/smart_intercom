import logging
from typing import Annotated

from fastapi import Depends

from src.client.interfaces import IS3SessionProvider
from src.client.storages.deps import get_s3_session_provider
from src.common.logger.deps import get_message_logger
from src.modules.messages.adapters.repositories.s3.message import MessageS3Repo
from src.modules.messages.interfaces import IMessageS3Repo


async def get_message_s3_repo(
    s3_session_provider: Annotated[
        IS3SessionProvider, Depends(get_s3_session_provider)
    ],
    logger: Annotated[logging.Logger, Depends(get_message_logger)],
) -> IMessageS3Repo:
    """
    Dependency injector for the message S3 repository instance.

    :param s3_session_provider: Provider for asynchronous S3 sessions.
    :param logger: Logger instance for message-related operations.
    :return: Message S3 repository instance implementing IMessageS3Repo.
    """

    return MessageS3Repo(s3_session_provider=s3_session_provider, logger=logger)
