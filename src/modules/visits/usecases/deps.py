from typing import Annotated

from fastapi import Depends

from src.modules.visits.interfaces import IVisitSrv, IVisitUC
from src.modules.visits.services.deps import get_visit_service
from src.modules.visits.usecases.constants import VisitUCConsts, VisitUCEnums
from src.modules.visits.usecases.constants.deps import (
    get_visit_uc_consts,
    get_visit_uc_enums,
)
from src.modules.visits.usecases.visit import VisitUC


async def get_visit_usecase(
    enums: Annotated[VisitUCEnums, Depends(get_visit_uc_enums)],
    consts: Annotated[VisitUCConsts, Depends(get_visit_uc_consts)],
    visit_service: Annotated[IVisitSrv, Depends(get_visit_service)],
) -> IVisitUC:
    return VisitUC(enums=enums, consts=consts, visit_service=visit_service)
