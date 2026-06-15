import logging

from src.client.storages.deps import get_postgres_session_provider
from src.config.settings.deps import get_settings
from src.workers.base import DependencyResolver
from src.workers.scheduler.runners.visit import VisitJobRunner


async def provide_visit_job_runner(logger: logging.Logger) -> VisitJobRunner:
    settings=get_settings()
    session_factory = (get_postgres_session_provider(settings)).get_session_factory()
    resolver = DependencyResolver(logger=logger)

    return VisitJobRunner(
        logger=logger,
        resolver=resolver,
        session_factory=session_factory,
    )
