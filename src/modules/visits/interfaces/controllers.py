from abc import ABC, abstractmethod

from fastapi import APIRouter


class IVisitController(ABC):
    """Interface for Visit controller operations.

    Defines the contract for all common visits-related API endpoints.
    """

    @property
    @abstractmethod
    def controller(self) -> APIRouter:
        """Get the configured APIRouter instance.

        :return: Configured FastAPI router with all meet routes
        """
        ...
