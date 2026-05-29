import logging

from src.client.interfaces import IS3SessionProvider
from src.common.adapters.repositories.s3 import S3BaseRepo
from src.modules.persons.interfaces import IPersonS3Repo


class PersonS3Repo(S3BaseRepo, IPersonS3Repo):
    """
    Person-specific S3 repository, implementing operations for person image storage.
    Inherits from S3BaseRepo for core S3 operations and implements IPersonS3Repo.
    """

    def __init__(self, s3_session_provider: IS3SessionProvider, logger: logging.Logger):
        """
        Initialize the PersonS3Repo instance.

        :param s3_session_provider: Provider for asynchronous S3 sessions.
        :param logger: Logger instance for person-related operations.
        """

        super().__init__(s3_session_provider=s3_session_provider, logger=logger)
        self._logger = logger
