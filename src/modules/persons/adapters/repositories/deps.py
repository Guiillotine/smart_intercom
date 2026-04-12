import logging
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.client.storages.deps import get_db
from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes_enums
from src.common.logger.deps import get_base_logger
from src.modules.persons.adapters.repositories import PersonPostgresRepo

from src.modules.persons.constants.enums import PersonTypeEnum
from src.modules.persons.interfaces import IPersonPostgresRepo


async def get_person_pg_repo(
    db: Annotated[AsyncSession, Depends(get_db)],
    logger: Annotated[logging.Logger, Depends(get_base_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
) -> IPersonPostgresRepo:
    return PersonPostgresRepo(
        db=db,
        logger=logger,
        errors=error_codes,
    )


async def get_employee_pg_repo(
    db: Annotated[AsyncSession, Depends(get_db)],
    logger: Annotated[logging.Logger, Depends(get_base_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
) -> IPersonPostgresRepo:
    return PersonPostgresRepo(
        db=db,
        logger=logger,
        errors=error_codes,
        person_type=PersonTypeEnum.EMPLOYEE,
    )

async def get_visitor_pg_repo(
    db: Annotated[AsyncSession, Depends(get_db)],
    logger: Annotated[logging.Logger, Depends(get_base_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
) -> IPersonPostgresRepo:
    return PersonPostgresRepo(
        db=db,
        logger=logger,
        errors=error_codes,
        person_type=PersonTypeEnum.VISITOR,
    )
