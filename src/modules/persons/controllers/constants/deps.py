from typing import Annotated

from fastapi import Depends

from src.common.constants import CommonEnums
from src.common.constants.deps import get_common_enums
from src.modules.persons.controllers.constants import EmployeeCtrlEnums


def get_employee_ctrl_enums(
    common_enums: Annotated[CommonEnums, Depends(get_common_enums)],
) ->  EmployeeCtrlEnums:
    return EmployeeCtrlEnums(
        common_enums=common_enums,
    )
