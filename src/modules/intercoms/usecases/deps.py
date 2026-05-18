import logging
from typing import Annotated

from fastapi import Depends

from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes_enums
from src.modules.intercoms.interfaces.usecases import IIntercomUC
from src.modules.intercoms.usecases import IntercomUC


async def get_intercom_usecase(
    enums: Annotated[IntercomUCEnums, Depends(get_intercom_usecase_enums)],
    errors: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
    logger: Annotated[logging.Logger, Depends(get_intercom_logger)],
    intercom_service: Annotated[IIntercomSrv, Depends(get_intercom_service)],
) -> IIntercomUC:
    """
    Dependency provider for the intercom use case layer.

    Initializes and returns a intercom use case instance with the required
    enums, error codes, logger, and service layer dependency.

    :return: IIntercomUC: The initialized intercom use case.
    """

    return IntercomUC(
        enums=enums,
        errors=errors,
        logger=logger,
        #intercom_service=intercom_service,
    )
