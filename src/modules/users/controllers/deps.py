from typing import Annotated

from fastapi import Depends

from src.modules.users.controllers.auth import AuthCtrl
from src.modules.users.controllers.constants import UserCtrlEnums
from src.modules.users.controllers.constants.deps import get_user_ctrl_enums
from src.modules.users.controllers.user import UserCtrl
from src.modules.users.interfaces import IAuthCtrl, IUserCtrl


def get_auth_controller(
    enums: Annotated[UserCtrlEnums, Depends(get_user_ctrl_enums)],
) -> IAuthCtrl:
    return AuthCtrl(enums=enums)


def get_user_controller(
    enums: Annotated[UserCtrlEnums, Depends(get_user_ctrl_enums)],
) -> IUserCtrl:
    return UserCtrl(enums=enums)
