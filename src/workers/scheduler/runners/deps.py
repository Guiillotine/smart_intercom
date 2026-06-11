import logging

from src.common.dependencies.storage import get_psql_session_provider
from src.workers.base import DependencyResolver
from src.workers.scheduler.runners.visit import VisitJobRunner


async def provide_visit_job_runner(logger: logging.Logger) -> VisitJobRunner:
    session_factory = (await get_psql_session_provider()).get_session_factory()
    resolver = DependencyResolver(logger=logger)

    return VisitJobRunner(
        logger=logger,
        resolver=resolver,
        session_factory=session_factory,
    )
