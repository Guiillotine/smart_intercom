from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile
from fastapi.params import Query, File, Body

from src.common.schemas import Msg
from src.modules.intercoms.controllers.constants import IntercomCtrlEnums
from src.modules.intercoms.interfaces import IIntercomController
from src.modules.intercoms.interfaces.usecases import IIntercomUC
from src.modules.intercoms.schemas.intercom import IntercomAnswer, Decision, \
    IntercomStartedVisit
from src.modules.intercoms.usecases.deps import get_intercom_usecase


class IntercomController(IIntercomController):
    """FastAPI controller for managing meets.

    Handles all intercoms-related operations including CRUD and membership management.
    """

    def __init__(
        self,
        enums: IntercomCtrlEnums,
    ):
        """Initialize the intercom controller.

        :param enums: Controller enums containing paths and request types
        """
        self._controller = APIRouter()
        self._enums = enums
        self._add_controllers()

    @property
    def controller(self) -> APIRouter:
        """Get the configured APIRouter instance.

        :return: Configured FastAPI router with all intercoms routes
        """
        return self._controller

    def _add_controllers(self) -> None:
        """Register all common intercoms endpoints to the router."""
        ...

    @staticmethod
    def start_visit(
        intercom_usecase: Annotated[IIntercomUC, Depends(get_intercom_usecase)],
    ) -> IntercomStartedVisit:
        # TODO:
        # 1. Get all unfinished visits
        # 2. Delete unfinished visits without data (no user messages) + s3
        # 3. Create new visit
        pass

    @staticmethod
    def process_visit_photo(
        visit_sid: Annotated[UUID, Query(alias="visitSid")],
        photo: Annotated[UploadFile, File(...)],
        intercom_usecase: Annotated[IIntercomUC, Depends(get_intercom_usecase)],
    ) -> Msg:
        # TODO:
        # 1. Process photo
        # 2. Call user if employee was detected
        pass

    @staticmethod
    def get_answer(
        visit_sid: Annotated[UUID, Query(alias="visitSid")],
        audio: Annotated[UploadFile, File(...)],
        intercom_usecase: Annotated[IIntercomUC, Depends(get_intercom_usecase)],
    ) -> IntercomAnswer:
        pass

    @staticmethod
    def get_answer_on_text_message(
        visit_sid: Annotated[UUID, Query(alias="visitSid")],
        message: Annotated[str, Body()],
        intercom_usecase: Annotated[IIntercomUC, Depends(get_intercom_usecase)],
    ) -> IntercomAnswer:
        # Get bot answer on text visitor message
        pass

    @staticmethod
    def get_user_decision(
        visit_sid: Annotated[UUID, Query(alias="visitSid")],
        audio: Annotated[UploadFile, File(...)],
        intercom_usecase: Annotated[IIntercomUC, Depends(get_intercom_usecase)],
    ) -> Decision:
        pass
