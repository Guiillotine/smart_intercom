import logging
from typing import Annotated

from fastapi import Depends

from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes_enums
from src.common.logger.deps import get_base_logger
from src.config.settings import Settings
from src.config.settings.deps import get_settings
from src.modules.persons.adapters.repositories.deps import get_employee_pg_repo, \
    get_visitor_pg_repo, get_person_pg_repo
from src.modules.persons.interfaces import IPersonPostgresRepo, IPersonSrv
from src.modules.persons.services.person import PersonSrv


async def get_person_service(
    logger: Annotated[logging.Logger, Depends(get_base_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
    settings: Annotated[Settings, Depends(get_settings)],
    person_postgres_repo: Annotated[IPersonPostgresRepo, Depends(get_person_pg_repo)],
) -> IPersonSrv:
    """
    Dependency provider for PersonSrv.

    :param logger: Configured logger instance.
    :param error_codes: Application error codes.
    :param settings: Settings.
    :param person_postgres_repo: Person repository.
    :return: Initialized person service instance.
    """

    return PersonSrv(
        errors=error_codes,
        logger=logger,
        settings=settings,
        person_postgres_repo=person_postgres_repo,
    )


async def get_employee_service(
    logger: Annotated[logging.Logger, Depends(get_base_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
    settings: Annotated[Settings, Depends(get_settings)],
    person_postgres_repo: Annotated[IPersonPostgresRepo, Depends(get_employee_pg_repo)],
) -> IPersonSrv:
    """
    Dependency provider for PersonSrv. Service only works with employees.

    :param logger: Configured logger instance.
    :param error_codes: Application error codes.
    :param settings: Settings.
    :param person_postgres_repo: Person repository working with employees.
    :return: Initialized person service instance.
    """

    return PersonSrv(
        errors=error_codes,
        logger=logger,
        settings=settings,
        person_postgres_repo=person_postgres_repo,
    )


async def get_visitor_service(
    logger: Annotated[logging.Logger, Depends(get_base_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
    settings: Annotated[Settings, Depends(get_settings)],
    person_postgres_repo: Annotated[IPersonPostgresRepo, Depends(get_visitor_pg_repo)],
) -> IPersonSrv:
    """
    Dependency provider for PersonSrv. Service only works with visitors.

    :param logger: Configured logger instance.
    :param error_codes: Application error codes.
    :param settings: Settings.
    :param person_postgres_repo: Person repository working with visitors.
    :return: Initialized person service instance.
    """

    return PersonSrv(
        errors=error_codes,
        logger=logger,
        settings=settings,
        person_postgres_repo=person_postgres_repo,
    )
