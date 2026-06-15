import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.config.settings import Settings
from src.workers.scheduler.interfaces import IScheduler
from src.workers.scheduler.runners import VisitJobRunner


class Scheduler(IScheduler):
    def __init__(
        self,
        logger: logging.Logger,
        settings: Settings,
        visit_job_runner: VisitJobRunner,
    ):
        """
        Initialize scheduler and register periodic background jobs.

        :param logger: Logger instance for scheduler operations.
        :param settings: Application settings containing scheduler intervals.
        :param visit_job_runner: Runner with visit-related scheduled jobs.
        """
        self._logger = logger
        self._scheduler = AsyncIOScheduler()
        # Visit
        self._scheduler.add_job(
            visit_job_runner.finish_waiting_decision_visits,
            trigger=IntervalTrigger(
                seconds=settings.scheduler.CALL_EMPLOYEE_TIMEOUT_SEC
            ),
        )

    @property
    def scheduler(self) -> AsyncIOScheduler:
        return self._scheduler
