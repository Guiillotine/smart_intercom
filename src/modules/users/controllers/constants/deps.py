from typing import Annotated

from fastapi import Depends

from src.common.constants import CommonEnums
from src.common.constants.deps import get_common_enums
from src.modules.users.controllers.constants import UserCtrlEnums


def get_user_ctrl_enums(
    common_enums: Annotated[CommonEnums, Depends(get_common_enums)],
) ->  UserCtrlEnums:
    return UserCtrlEnums(
        common_enums=common_enums,
    )
