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

api_controller.include_router(
    get_auth_controller(
        enums=get_user_ctrl_enums(common_enums=common_enums),
    ).controller,
    tags=["Auth"],
    prefix="/auth",
)

api_controller.include_router(
    get_user_controller(
        enums=get_user_ctrl_enums(common_enums=common_enums),
    ).controller,
    tags=["Users"],
    prefix="/users",
)

api_controller.include_router(
    get_visit_controller(
        enums=get_visit_ctrl_enums(common_enums=common_enums),
    ).controller,
    tags=["Visits"],
    prefix="/visits",
)

api_controller.include_router(
    get_message_controller(
        enums=get_message_ctrl_enums(common_enums=common_enums),
    ).controller,
    tags=["Messages"],
    prefix="/messages",
)

api_controller.include_router(
    get_intercom_controller(
        enums=get_intercom_ctrl_enums(common_enums=common_enums),
    ).controller,
    tags=["Intercoms"],
    prefix="/intercoms",
)
