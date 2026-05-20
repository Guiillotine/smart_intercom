import logging
from typing import Annotated

from fastapi import Depends
from faster_whisper import WhisperModel

from src.config.settings import Settings
from src.config.settings.deps import get_settings
from src.modules.speech.adapters.whisper.deps import get_whisper_model
from src.modules.speech.services import ASRService


def get_asr_service(
    settings: Annotated[Settings, Depends(get_settings)],
    logger: Annotated[logging.Logger, Depends(get_speech_logger)],
    consts: Annotated[ASRServiceConsts, Depends(get_asr_service_consts)],
    whisper_model: Annotated[WhisperModel, Depends(get_whisper_model)],
) -> IASRService:
    return ASRService(
        consts=consts,
        logger=logger,
        settings=settings,
        model=whisper_model,
    )
