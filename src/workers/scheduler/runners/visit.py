import logging
from collections.abc import Callable

from src.modules.visits.usecases.deps import get_visit_usecase
from src.workers.base import DependencyResolver


class VisitJobRunner:
    def __init__(
        self,
        logger: logging.Logger,
        resolver: DependencyResolver,
        session_factory: Callable,
    ):
        self._logger = logger
        self._resolver = resolver
        self._session_factory = session_factory

    async def finish_waiting_decision_visits(self) -> None:
        async with (
            self._session_factory() as db,
            DependencyResolver(self._logger) as res,
        ):
            uc = await res.resolve(
                get_visit_usecase,
                db=db,
            )
            await uc.finish_waiting_decision_visits()
