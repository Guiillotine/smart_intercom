from fastapi import APIRouter

from src.common.constants.deps import get_common_enums
from src.modules.persons.controllers import get_employee_controller
from src.modules.persons.controllers.constants.deps import get_employee_ctrl_enums


api_controller = APIRouter()

api_controller.include_router(
    get_employee_controller(
        enums=get_employee_ctrl_enums(
            common_enums=get_common_enums(),
        ),
    ).controller,
    tags=["Employees"],
    prefix="/employees",
)
