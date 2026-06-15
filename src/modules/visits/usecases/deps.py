import logging
from typing import Annotated

from fastapi import Depends

from src.common.helpers.deps import get_custom_datetime
from src.common.interfaces import ICustomDateTime
from src.common.logger.deps import get_visit_logger
from src.config.settings import Settings
from src.config.settings.deps import get_settings
from src.modules.visits.interfaces import IVisitSrv, IVisitUC
from src.modules.visits.services.deps import get_visit_service
from src.modules.visits.usecases.constants import VisitUCConsts, VisitUCEnums
from src.modules.visits.usecases.constants.deps import (
    get_visit_uc_consts,
    get_visit_uc_enums,
)
from src.modules.visits.usecases.visit import VisitUC


async def get_visit_usecase(
    logger: Annotated[logging.Logger, Depends(get_visit_logger)],
    enums: Annotated[VisitUCEnums, Depends(get_visit_uc_enums)],
    consts: Annotated[VisitUCConsts, Depends(get_visit_uc_consts)],
    settings: Annotated[Settings, Depends(get_settings)],
    custom_datetime: Annotated[ICustomDateTime, Depends(get_custom_datetime)],
    visit_service: Annotated[IVisitSrv, Depends(get_visit_service)],
) -> IVisitUC:
    return VisitUC(
        logger=logger,
        enums=enums,
        consts=consts,
        settings=settings,
        custom_datetime=custom_datetime,
        visit_service=visit_service,
    )
