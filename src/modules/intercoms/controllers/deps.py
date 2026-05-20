from typing import Annotated

from fastapi import Depends

from src.modules.intercoms.controllers.constants import IntercomCtrlEnums
from src.modules.intercoms.controllers.constants.deps import get_intercom_ctrl_enums
from src.modules.intercoms.controllers.intercom import IntercomController
from src.modules.intercoms.interfaces import IIntercomController


def get_intercom_controller(
    enums: Annotated[IntercomCtrlEnums, Depends(get_intercom_ctrl_enums)],
) -> IIntercomController:
    return IntercomController(enums=enums)
