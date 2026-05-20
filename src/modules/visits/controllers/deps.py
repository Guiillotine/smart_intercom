from typing import Annotated

from fastapi import Depends

from src.modules.visits.controllers.constants import VisitCtrlEnums
from src.modules.visits.controllers.constants.deps import get_visit_ctrl_enums
from src.modules.visits.controllers.visit import VisitController
from src.modules.visits.interfaces import IVisitController


def get_visit_controller(
    enums: Annotated[VisitCtrlEnums, Depends(get_visit_ctrl_enums)],
) -> IVisitController:
    return VisitController(enums=enums)
