from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.common.deps import get_user_sid
from src.modules.messages.controllers.constants import MessageCtrlEnums
from src.modules.messages.interfaces import IMessageCtrl
from src.modules.messages.schemas import MessageInHistory


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
            response_model=MessageInHistory,
        )

    @staticmethod
    async def get_visit_message_history(
        user_sid: Annotated[UUID, Depends(get_user_sid)],
        visit_sid: Annotated[UUID, Query(alias="visitSid")],
        message_usecase: Annotated[IMessageUC, Depends(get_message_usecase)],
    ) -> MessageInHistory:
        """
        Get visit message history.

        ## Notes:
        - Messages are sorted by datetime from oldest to newest.
        """

        return await message_usecase.get_message_history(
            user_sid=user_sid,
            visit_sid=visit_sid,
        )
