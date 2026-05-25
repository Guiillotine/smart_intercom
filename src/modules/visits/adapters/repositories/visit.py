import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.common.adapters.repositories.postgres import PostgresBaseRepo
from src.common.constants import ErrorCodesEnums
from src.modules.visits.interfaces import IVisitPersonPostgresRepo, IVisitPostgresRepo
from src.modules.visits.models import VisitModel, VisitPersonModel
from src.modules.visits.schemas import VisitCreate, VisitPersonCreate, VisitUpdate
from src.modules.visits.adapters.repositories.constants import (
    VisitRepoConsts,
    VisitRepoEnums,
)


class VisitPostgresRepo(
    PostgresBaseRepo[VisitModel, VisitCreate, VisitUpdate], IVisitPostgresRepo
):
    def __init__(
        self,
        db: AsyncSession,
        errors: ErrorCodesEnums,
        logger: logging.Logger,
        enums: VisitRepoEnums,
        consts: VisitRepoConsts,
    ):
        super().__init__(db=db, model=VisitModel, errors=errors, logger=logger)
        self._enums = enums
        self._consts = consts


class VisitPersonPostgresRepo(
    PostgresBaseRepo[VisitPersonModel, VisitPersonCreate, VisitPersonCreate],
    IVisitPersonPostgresRepo,
):
    def __init__(
        self,
        db: AsyncSession,
        errors: ErrorCodesEnums,
        logger: logging.Logger,
        enums: VisitRepoEnums,
        consts: VisitRepoConsts,
    ):
        super().__init__(db=db, model=VisitPersonModel, errors=errors, logger=logger)
        self._enums = enums
        self._consts = consts
