from typing import Annotated

from fastapi import Depends

from src.common.constants import CommonEnums
from src.common.constants.deps import get_common_enums
from src.modules.visits.controllers.constants import VisitCtrlEnums


def get_visit_ctrl_enums(
    common_enums: Annotated[CommonEnums, Depends(get_common_enums)],
) ->  VisitCtrlEnums:
    return VisitCtrlEnums(
        common_enums=common_enums,
    )
