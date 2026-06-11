import logging

from src.config.settings.deps import get_settings
from src.workers.scheduler import Scheduler
from src.workers.scheduler.interfaces import IScheduler
from src.workers.scheduler.runners.deps import provide_visit_job_runner


async def provide_scheduler(logger: logging.Logger) -> IScheduler:
    """
    Build scheduler instance.

    :return: Instance of Scheduler implementing IScheduler interface.
    """
    return Scheduler(
        logger=logger,
        settings=get_settings(),
        visit_job_runner=await provide_visit_job_runner(logger=logger),
    )
