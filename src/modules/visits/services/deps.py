import logging
from typing import Annotated

from fastapi import Depends

from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes_enums
from src.common.logger.deps import get_visit_logger
from src.modules.visits.adapters.repositories.deps import get_visit_pg_repo
from src.modules.visits.interfaces import IVisitPostgresRepo, IVisitSrv
from src.modules.visits.services.constants import VisitSrvConsts, VisitSrvEnums
from src.modules.visits.services.constants.deps import (
    get_visit_srv_consts,
    get_visit_srv_enums,
)
from src.modules.visits.services.visit import VisitSrv


async def get_visit_service(
    logger: Annotated[logging.Logger, Depends(get_visit_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
    enums: Annotated[VisitSrvEnums, Depends(get_visit_srv_enums)],
    consts: Annotated[VisitSrvConsts, Depends(get_visit_srv_consts)],
    visit_repo: Annotated[IVisitPostgresRepo, Depends(get_visit_pg_repo)],
) -> IVisitSrv:
    return VisitSrv(
        errors=error_codes,
        enums=enums,
        consts=consts,
        logger=logger,
        visit_repo=visit_repo,
    )
