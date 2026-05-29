import logging
from typing import Annotated

from fastapi import Depends

from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes_enums
from src.common.logger.deps import get_base_logger
from src.config.settings import Settings
from src.config.settings.deps import get_settings
from src.modules.persons.adapters.postgres.deps import get_employee_pg_repo, \
    get_visitor_pg_repo, get_person_pg_repo
from src.modules.persons.adapters.repositories.s3.deps import get_person_s3_repo
from src.modules.persons.interfaces import IPersonPostgresRepo, IPersonSrv, \
    IPersonS3Repo
from src.modules.persons.services.constants import PersonSrvEnums
from src.modules.persons.services.constants.deps import get_person_srv_enums
from src.modules.persons.services.person import PersonSrv


async def get_person_service(
    logger: Annotated[logging.Logger, Depends(get_base_logger)],
    enums: Annotated[PersonSrvEnums, Depends(get_person_srv_enums)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
    settings: Annotated[Settings, Depends(get_settings)],
    person_s3_repo: Annotated[IPersonS3Repo, Depends(get_person_s3_repo)],
    person_postgres_repo: Annotated[IPersonPostgresRepo, Depends(get_person_pg_repo)],
) -> IPersonSrv:
    """
    Dependency provider for PersonSrv.
    """
    return PersonSrv(
        logger=logger,
        enums=enums,
        errors=error_codes,
        settings=settings,
        person_s3_repo=person_s3_repo,
        person_postgres_repo=person_postgres_repo,
    )


async def get_employee_service(
    logger: Annotated[logging.Logger, Depends(get_base_logger)],
    enums: Annotated[PersonSrvEnums, Depends(get_person_srv_enums)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
    settings: Annotated[Settings, Depends(get_settings)],
    person_s3_repo: Annotated[IPersonS3Repo, Depends(get_person_s3_repo)],
    person_postgres_repo: Annotated[IPersonPostgresRepo, Depends(get_employee_pg_repo)],
) -> IPersonSrv:
    """
    Dependency provider for PersonSrv. Service only works with employees.
    """

    return PersonSrv(
        logger=logger,
        enums=enums,
        errors=error_codes,
        settings=settings,
        person_s3_repo=person_s3_repo,
        person_postgres_repo=person_postgres_repo,
    )


async def get_visitor_service(
    logger: Annotated[logging.Logger, Depends(get_base_logger)],
    enums: Annotated[PersonSrvEnums, Depends(get_person_srv_enums)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
    settings: Annotated[Settings, Depends(get_settings)],
    person_s3_repo: Annotated[IPersonS3Repo, Depends(get_person_s3_repo)],
    person_postgres_repo: Annotated[IPersonPostgresRepo, Depends(get_visitor_pg_repo)],
) -> IPersonSrv:
    """
    Dependency provider for PersonSrv. Service only works with visitors.
    """

    return PersonSrv(
        logger=logger,
        enums=enums,
        errors=error_codes,
        settings=settings,
        person_s3_repo=person_s3_repo,
        person_postgres_repo=person_postgres_repo,
    )
