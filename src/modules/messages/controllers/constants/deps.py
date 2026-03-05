from typing import Annotated

from fastapi import Depends

from src.common.constants import CommonEnums
from src.common.constants.deps import get_common_enums
from src.modules.messages.controllers.constants import MessageCtrlEnums


def get_message_ctrl_enums(
    common_enums: Annotated[CommonEnums, Depends(get_common_enums)],
) ->  MessageCtrlEnums:
    return MessageCtrlEnums(
        common_enums=common_enums,
    )
