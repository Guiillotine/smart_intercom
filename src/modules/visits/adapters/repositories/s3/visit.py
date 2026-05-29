import logging

from src.client.interfaces import IS3SessionProvider
from src.common.adapters.repositories.s3 import S3BaseRepo
from src.modules.visits.interfaces import IVisitS3Repo


class VisitS3Repo(S3BaseRepo, IVisitS3Repo):
    """
    Visit-specific S3 repository, implementing operations for visit image storage.
    Inherits from S3BaseRepo for core S3 operations and implements IVisitS3Repo.
    """

    def __init__(self, s3_session_provider: IS3SessionProvider, logger: logging.Logger):
        """
        Initialize the VisitS3Repo instance.

        :param s3_session_provider: Provider for asynchronous S3 sessions.
        :param logger: Logger instance for visit-related operations.
        """

        super().__init__(s3_session_provider=s3_session_provider, logger=logger)
        self._logger = logger
