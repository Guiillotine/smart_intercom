from typing import Annotated

from fastapi import Depends

from src.modules.persons.controllers.constants import EmployeeCtrlEnums
from src.modules.persons.controllers.constants.deps import get_employee_ctrl_enums
from src.modules.persons.controllers.employee import EmployeeCtrl
from src.modules.persons.interfaces import IEmployeeCtrl


def get_employee_controller(
    enums: Annotated[EmployeeCtrlEnums, Depends(get_employee_ctrl_enums)],
) -> IEmployeeCtrl:
    """
    Factory function to provide an employee controller instance.

    :return: Initialized employee controller.
    """

    return EmployeeCtrl(enums=enums)
