import logging
from typing import Annotated

from fastapi import Depends

from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes_enums
from src.modules.intercoms.interfaces.usecases import IIntercomUC
from src.modules.intercoms.usecases import IntercomUC
from src.modules.intercoms.usecases.constants import IntercomUCConsts
from src.modules.intercoms.usecases.constants.deps import get_intercom_usecase_enums, \
    get_intercom_usecase_consts


async def get_intercom_usecase(
    enums: Annotated[IntercomUCEnums, Depends(get_intercom_usecase_enums)],
    consts: Annotated[IntercomUCConsts, Depends(get_intercom_usecase_consts)],
    errors: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
    logger: Annotated[logging.Logger, Depends(get_intercom_logger)],
    intercom_service: Annotated[IIntercomSrv, Depends(get_intercom_service)],
    visit_service: Annotated[IVisitSrv, Depends(get_visit_service)],
    message_service: Annotated[IMessageSrv, Depends(get_message_service)],
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
        settings=settings,
        asr_service=asr_service,
        tts_service=tts_service,
        visit_service=visit_service,
        dialog_service=dialog_service,
        message_service=message_service,
    )
