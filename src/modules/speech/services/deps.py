import logging
from typing import Annotated

from fastapi import Depends
from faster_whisper import WhisperModel

from src.common.logger.deps import get_speech_logger
from src.config.settings import Settings
from src.config.settings.deps import get_settings
from src.modules.speech.adapters.whisper.deps import get_whisper_model
from src.modules.speech.handlers import TTSModelManager
from src.modules.speech.handlers.deps import get_tts_model_manager
from src.modules.speech.interfaces import ITTSSrv, IASRSrv
from src.modules.speech.services import ASRSrv, TTSSrv
from src.modules.speech.services.constants import ASRServiceConsts
from src.modules.speech.services.constants.deps import get_asr_service_consts


def get_asr_service(
    settings: Annotated[Settings, Depends(get_settings)],
    logger: Annotated[logging.Logger, Depends(get_speech_logger)],
    consts: Annotated[ASRServiceConsts, Depends(get_asr_service_consts)],
    whisper_model: Annotated[WhisperModel, Depends(get_whisper_model)],
) -> IASRSrv:
    return ASRSrv(
        consts=consts,
        logger=logger,
        settings=settings,
        model=whisper_model,
    )


def get_tts_service(
    logger: Annotated[logging.Logger, Depends(get_speech_logger)],
    settings: Settings = Depends(get_settings),
    tts_model_manager: TTSModelManager = Depends(get_tts_model_manager),
) -> ITTSSrv:
    return TTSSrv(
        logger=logger,
        settings=settings,
        tts_model_manager=tts_model_manager,
    )
