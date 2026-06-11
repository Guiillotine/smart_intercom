from abc import ABC, abstractmethod

from apscheduler.schedulers.asyncio import AsyncIOScheduler


class IScheduler(ABC):
    @property
    @abstractmethod
    def scheduler(self) -> AsyncIOScheduler:
        """Get scheduler."""
        ...
