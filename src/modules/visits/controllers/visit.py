from fastapi import APIRouter

from src.modules.visits.controllers.constants import VisitCtrlEnums
from src.modules.visits.interfaces import IVisitController


class VisitController(IVisitController):
    """FastAPI controller for managing meets.

    Handles all visits-related operations including CRUD and membership management.
    """

    def __init__(
        self,
        enums: VisitCtrlEnums,
    ):
        """Initialize the visit controller.

        :param enums: Controller enums containing paths and request types
        """
        self._controller = APIRouter()
        self._enums = enums
        self._add_controllers()

    @property
    def controller(self) -> APIRouter:
        """Get the configured APIRouter instance.

        :return: Configured FastAPI router with all visits routes
        """
        return self._controller

    def _add_controllers(self) -> None:
        """Register all common visits endpoints to the router."""
        ...
