import logging
from typing import Annotated

from fastapi import Depends

from src.client.interfaces import IS3SessionProvider
from src.client.storages.deps import get_s3_session_provider
from src.common.logger.deps import get_person_logger
from src.modules.persons.adapters.repositories.s3.person import PersonS3Repo
from src.modules.persons.interfaces import IPersonS3Repo


async def get_person_s3_repo(
    s3_session_provider: Annotated[
        IS3SessionProvider, Depends(get_s3_session_provider)
    ],
    logger: Annotated[logging.Logger, Depends(get_person_logger)],
) -> IPersonS3Repo:
    """
    Dependency injector for the person S3 repository instance.

    :param s3_session_provider: Provider for asynchronous S3 sessions.
    :param logger: Logger instance for person-related operations.
    :return: Person S3 repository instance implementing IPersonS3Repo.
    """

    return PersonS3Repo(s3_session_provider=s3_session_provider, logger=logger)
