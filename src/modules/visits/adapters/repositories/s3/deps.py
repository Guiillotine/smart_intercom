import logging
from typing import Annotated

from fastapi import Depends

from src.client.interfaces import IS3SessionProvider
from src.client.storages.deps import get_s3_session_provider
from src.common.logger.deps import get_visit_logger
from src.modules.visits.adapters.repositories.s3.visit import VisitS3Repo
from src.modules.visits.interfaces import IVisitS3Repo


async def get_visit_s3_repo(
    s3_session_provider: Annotated[
        IS3SessionProvider, Depends(get_s3_session_provider)
    ],
    logger: Annotated[logging.Logger, Depends(get_visit_logger)],
) -> IVisitS3Repo:
    """
    Dependency injector for the visit S3 repository instance.

    :param s3_session_provider: Provider for asynchronous S3 sessions.
    :param logger: Logger instance for visit-related operations.
    :return: Visit S3 repository instance implementing IVisitS3Repo.
    """

    return VisitS3Repo(s3_session_provider=s3_session_provider, logger=logger)
