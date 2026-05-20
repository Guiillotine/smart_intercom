from typing import Annotated

from fastapi import Depends

from src.modules.messages.controllers.constants import MessageCtrlEnums
from src.modules.messages.controllers.constants.deps import get_message_ctrl_enums
from src.modules.messages.controllers.message import MessageCtrl
from src.modules.messages.interfaces import IMessageCtrl


def get_message_controller(
    enums: Annotated[MessageCtrlEnums, Depends(get_message_ctrl_enums)],
) -> IMessageCtrl:
    return MessageCtrl(enums=enums)
