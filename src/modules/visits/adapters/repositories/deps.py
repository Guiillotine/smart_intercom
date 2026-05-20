import logging
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.client.storages.deps import get_db
from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes_enums
from src.common.logger.deps import get_visit_logger
from src.modules.visits.adapters.repositories.constants import VisitRepoConsts, VisitRepoEnums
from src.modules.visits.adapters.repositories.constants.deps import (
    get_visit_repo_consts,
    get_visit_repo_enums,
)
from src.modules.visits.adapters.repositories.visit import (
    VisitPersonPostgresRepo,
    VisitPostgresRepo,
)
from src.modules.visits.interfaces import IVisitPersonPostgresRepo, IVisitPostgresRepo


async def get_visit_pg_repo(
    db: Annotated[AsyncSession, Depends(get_db)],
    logger: Annotated[logging.Logger, Depends(get_visit_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
    enums: Annotated[VisitRepoEnums, Depends(get_visit_repo_enums)],
    consts: Annotated[VisitRepoConsts, Depends(get_visit_repo_consts)],
) -> IVisitPostgresRepo:
    return VisitPostgresRepo(
        db=db,
        logger=logger,
        errors=error_codes,
        enums=enums,
        consts=consts,
    )


async def get_visit_person_pg_repo(
    db: Annotated[AsyncSession, Depends(get_db)],
    logger: Annotated[logging.Logger, Depends(get_visit_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
    enums: Annotated[VisitRepoEnums, Depends(get_visit_repo_enums)],
    consts: Annotated[VisitRepoConsts, Depends(get_visit_repo_consts)],
) -> IVisitPersonPostgresRepo:
    return VisitPersonPostgresRepo(
        db=db,
        logger=logger,
        errors=error_codes,
        enums=enums,
        consts=consts,
    )
