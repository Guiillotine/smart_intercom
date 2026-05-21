import logging

from src.client.interfaces import IS3SessionProvider
from src.common.adapters.repositories.s3 import S3BaseRepo
from src.modules.messages.interfaces import IMessageS3Repo


class MessageS3Repo(S3BaseRepo, IMessageS3Repo):
    """
    Message-specific S3 repository, implementing operations for message image storage.
    Inherits from S3BaseRepo for core S3 operations and implements IMessageS3Repo.
    """

    def __init__(self, s3_session_provider: IS3SessionProvider, logger: logging.Logger):
        """
        Initialize the MessageS3Repo instance.

        :param s3_session_provider: Provider for asynchronous S3 sessions.
        :param logger: Logger instance for message-related operations.
        """

        super().__init__(s3_session_provider=s3_session_provider, logger=logger)
        self._logger = logger
