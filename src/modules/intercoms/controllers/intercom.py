from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile
from fastapi.params import Query, File, Body

from src.modules.intercoms.controllers.constants import IntercomCtrlEnums
from src.modules.intercoms.interfaces import IIntercomController
from src.modules.intercoms.interfaces.usecases import IIntercomUC
from src.modules.intercoms.schemas.intercom import (
    Decision,
    IntercomAnswer,
    IntercomStartedVisit,
    PhotoProcessingResult, IntercomAnswerWithText,
)
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

        self._controller.add_api_route(
            path=self._enums.IntercomCtrlPath.start_visit,
            endpoint=self.start_visit,
            methods=[self._enums.Common.RequestType.POST],
            response_model=IntercomStartedVisit,
        )
        
        self._controller.add_api_route(
            path=self._enums.IntercomCtrlPath.process_visit_photo,
            endpoint=self.process_visit_photo,
            methods=[self._enums.Common.RequestType.POST],
            response_model=PhotoProcessingResult,
        )
        
        self._controller.add_api_route(
            path=self._enums.IntercomCtrlPath.get_answer,
            endpoint=self.get_answer,
            methods=[self._enums.Common.RequestType.POST],
            response_model=IntercomAnswer,
        )
        
        self._controller.add_api_route(
            path=self._enums.IntercomCtrlPath.get_answer_on_text_message,
            endpoint=self.get_answer_on_text_message,
            methods=[self._enums.Common.RequestType.POST],
            response_model=IntercomAnswerWithText,
        )
        
        self._controller.add_api_route(
            path=self._enums.IntercomCtrlPath.get_user_decision,
            endpoint=self.get_user_decision,
            methods=[self._enums.Common.RequestType.GET],
            response_model=Decision,
        )

    @staticmethod
    async def start_visit(
        intercom_usecase: Annotated[IIntercomUC, Depends(get_intercom_usecase)],
    ) -> IntercomStartedVisit:
        """Start a new intercom visit and return the greeting audio path."""
        return await intercom_usecase.start_visit()

    @staticmethod
    async def process_visit_photo(
        visit_sid: Annotated[UUID, Query(alias="visitSid")],
        photo: Annotated[UploadFile, File(...)],
        intercom_usecase: Annotated[IIntercomUC, Depends(get_intercom_usecase)],
    ) -> PhotoProcessingResult:
        """Analyze a visit photo and register detected visitors."""
        return await intercom_usecase.process_visit_photo(visit_sid, photo)

    @staticmethod
    async def get_answer(
        visit_sid: Annotated[UUID, Query(alias="visitSid")],
        audio: Annotated[UploadFile, File(...)],
        intercom_usecase: Annotated[IIntercomUC, Depends(get_intercom_usecase)],
    ) -> IntercomAnswer:
        return await intercom_usecase.get_answer(
            audio=audio,
            visit_sid=visit_sid,
        )

    @staticmethod
    async def get_answer_on_text_message(
        visit_sid: Annotated[UUID, Query(alias="visitSid")],
        message: Annotated[str, Body()],
        intercom_usecase: Annotated[IIntercomUC, Depends(get_intercom_usecase)],
    ) -> IntercomAnswerWithText:
        return await intercom_usecase.get_answer_on_text_message(
            message=message,
            visit_sid=visit_sid,
        )

    @staticmethod
    async def get_user_decision(
        visit_sid: Annotated[UUID, Query(alias="visitSid")],
        intercom_usecase: Annotated[IIntercomUC, Depends(get_intercom_usecase)],
    ) -> Decision:
        return await intercom_usecase.get_user_decision(visit_sid)
