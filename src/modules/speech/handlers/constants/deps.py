from typing import Annotated

from fastapi import Depends

from src.config.settings import Settings
from src.config.settings.deps import get_settings
from src.modules.speech.handlers import TTSModelManager
from src.modules.speech.handlers.constants.consts import TTSModelManagerConsts
from src.modules.speech.interfaces import ITTSModelManager


def get_tts_model_manager_consts(
    settings: Annotated[Settings, Depends(get_settings)],
) -> TTSModelManagerConsts:
    return TTSModelManagerConsts(settings=settings)
