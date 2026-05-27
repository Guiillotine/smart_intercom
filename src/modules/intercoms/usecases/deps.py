import logging
from typing import Annotated

from fastapi import Depends

from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes_enums
from src.common.helpers.deps import get_custom_datetime
from src.common.interfaces import ICustomDateTime
from src.common.logger.deps import get_intercom_logger
from src.config.settings import Settings
from src.config.settings.deps import get_settings
from src.modules.dialogues.interfaces import IDialogueSrv
from src.modules.dialogues.services.deps import get_dialogue_service
from src.modules.faces.interfaces import IFaceAnalyzerSrv
from src.modules.faces.services.deps import get_face_analyzer_service
from src.modules.intercoms.interfaces.usecases import IIntercomUC
from src.modules.intercoms.usecases import IntercomUC
from src.modules.intercoms.usecases.constants import IntercomUCConsts, IntercomUCEnums
from src.modules.intercoms.usecases.constants.deps import get_intercom_usecase_enums, \
    get_intercom_usecase_consts
from src.modules.messages.interfaces import IMessageSrv
from src.modules.messages.services.deps import get_message_service
from src.modules.persons.interfaces import IPersonSrv
from src.modules.persons.services.deps import get_person_service
from src.modules.speech.interfaces import ITTSSrv, IASRSrv
from src.modules.speech.services.deps import get_tts_service, get_asr_service
from src.modules.visits.interfaces import IVisitSrv
from src.modules.visits.services.deps import get_visit_service


async def get_intercom_usecase(
    logger: Annotated[logging.Logger, Depends(get_intercom_logger)],
    enums: Annotated[IntercomUCEnums, Depends(get_intercom_usecase_enums)],
    consts: Annotated[IntercomUCConsts, Depends(get_intercom_usecase_consts)],
    errors: Annotated[ErrorCodesEnums, Depends(get_error_codes_enums)],
    settings: Annotated[Settings, Depends(get_settings)],
    asr_service: Annotated[IASRSrv, Depends(get_asr_service)],
    tts_service: Annotated[ITTSSrv, Depends(get_tts_service)],
    visit_service: Annotated[IVisitSrv, Depends(get_visit_service)],
    person_service: Annotated[IPersonSrv, Depends(get_person_service)],
    message_service: Annotated[IMessageSrv, Depends(get_message_service)],
    custom_datetime: Annotated[ICustomDateTime, Depends(get_custom_datetime)],
    dialogue_service: Annotated[IDialogueSrv, Depends(get_dialogue_service)],
    face_analyzer_service: Annotated[
        IFaceAnalyzerSrv, Depends(get_face_analyzer_service)
    ],
) -> IIntercomUC:
    """
    Dependency provider for the intercom use case layer.

    Initializes and returns an intercom use case instance with the required
    enums, error codes, logger, and service layer dependency.

    :return: IIntercomUC: The initialized intercom use case.
    """

    return IntercomUC(
        enums=enums,
        consts=consts,
        errors=errors,
        logger=logger,
        settings=settings,
        asr_service=asr_service,
        tts_service=tts_service,
        visit_service=visit_service,
        message_service=message_service,
        custom_datetime=custom_datetime,
        dialogue_service=dialogue_service,
        face_analyzer_service=face_analyzer_service,
    )
