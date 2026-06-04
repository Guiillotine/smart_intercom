from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.common.deps.user_sid import require_admin
from src.common.schemas import PaginationResult, Pagination
from src.modules.messages.controllers.constants import MessageCtrlEnums
from src.modules.messages.interfaces import IMessageCtrl
from src.modules.messages.interfaces.usecases import IMessageUC
from src.modules.messages.schemas import MessageInHistory
from src.modules.messages.usecases.deps import get_message_usecase


class MessageCtrl(IMessageCtrl):
    """
    Routing class for message-related API endpoints.
    """

    def __init__(
        self,
        enums: MessageCtrlEnums,
    ):
        """
        Initializes the MessageRouters instance.

        Sets up an internal FastAPI APIRouter and binds all message-related
        routes.
        """

        self._controller = APIRouter()
        self._enums = enums
        self._add_controllers()

    @property
    def controller(self) -> APIRouter:
        """
        Returns the FastAPI router instance with all registered message endpoints.

        :return: Configured APIRouter for inclusion in the main FastAPI application.
        """

        return self._controller

    def _add_controllers(self) -> None:
        """
        Registers all message-related routes to the internal router instance.
        """

        self._controller.add_api_route(
            path=self._enums.MessageCtrlPath.get_visit_message_history,
            endpoint=self.get_visit_message_history,
            methods=[self._enums.Common.RequestType.GET],
            response_model=PaginationResult[MessageInHistory],
        )

    @staticmethod
    async def get_visit_message_history(
        user_sid: Annotated[UUID, Depends(require_admin)],
        visit_sid: Annotated[UUID, Query(alias="visitSid")],
        pagination_params: Annotated[Pagination, Depends(Pagination)],
        message_usecase: Annotated[IMessageUC, Depends(get_message_usecase)],
    ) -> PaginationResult[MessageInHistory]:
        """
        Get visit message history.

        ## Notes:
        - Messages are sorted by datetime from oldest to newest.
        """

        return await message_usecase.get_message_history(
            user_sid=user_sid,
            visit_sid=visit_sid,
            pagination_params=pagination_params,
        )
