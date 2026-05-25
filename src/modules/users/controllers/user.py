from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.common.deps import get_user_sid
from src.modules.users.controllers.constants import UserCtrlEnums
from src.modules.users.interfaces import IUserCtrl, IUserUC
from src.modules.users.schemas import UserWithRole
from src.modules.users.usecases.deps import get_user_usecase


class UserCtrl(IUserCtrl):
    """
    Routing class for user-related API endpoints.
    """

    def __init__(
        self,
        enums: UserCtrlEnums,
    ):
        """
        Initializes the UserRouters instance.

        Sets up an internal FastAPI APIRouter and binds all user-related
        routes.
        """

        self._controller = APIRouter()
        self._enums = enums
        self._add_controllers()

    @property
    def controller(self) -> APIRouter:
        """
        Returns the FastAPI router instance with all registered user endpoints.

        :return: Configured APIRouter for inclusion in the main FastAPI application.
        """

        return self._controller

    def _add_controllers(self) -> None:
        """
        Registers all user-related routes to the internal router instance.
        """

        self._controller.add_api_route(
            path=self._enums.UserCtrlPath.me,
            endpoint=self.me,
            methods=[self._enums.Common.RequestType.GET],
            response_model=UserWithRole,
        )

        self._controller.add_api_route(
            path=self._enums.UserCtrlPath.get_user,
            endpoint=self.get_user,
            methods=[self._enums.Common.RequestType.GET],
            response_model=UserWithRole,
        )

    @staticmethod
    async def me(
        user_sid: Annotated[UUID, Depends(get_user_sid)],
        user_usecase: Annotated[IUserUC, Depends(get_user_usecase)],
    ) -> UserWithRole:
        """
        Get current user info.

        ## Returns:
        - Current user info with role.
        """
        return await user_usecase.get_user_info(user_sid)

    @staticmethod
    async def get_user(
        sid: Annotated[UUID, Query(alias="userSid")],
        user_sid: Annotated[UUID, Depends(get_user_sid)],
        user_usecase: Annotated[IUserUC, Depends(get_user_usecase)],
    ) -> UserWithRole:
        """
        Get user by sid.

        ## Returns:
        - User info with role.
        """
        return await user_usecase.get_by_sid(sid=sid, user_sid=user_sid)
