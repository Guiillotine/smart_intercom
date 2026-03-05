from typing import Annotated

from fastapi import Depends

from src.common.constants import CommonEnums
from src.common.constants.deps import get_common_enums
from src.modules.intercoms.controllers.constants import IntercomCtrlEnums


def get_intercom_ctrl_enums(
    common_enums: Annotated[CommonEnums, Depends(get_common_enums)],
) ->  IntercomCtrlEnums:
    return IntercomCtrlEnums(
        common_enums=common_enums,
    )
