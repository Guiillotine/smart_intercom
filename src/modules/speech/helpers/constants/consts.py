import os
from pathlib import Path

from src.common.constants.enums import LanguageEnum
from src.config.settings import Settings
from src.modules.speech.schemas import TTSModelParams

class RepoDirConsts:
    PATH: Path = Path("").resolve() / "vendor" / "silero-models"


class TTSModelManagerConsts:
    def __init__(self, settings: Settings):
        self.LangTTSModelMap: dict[LanguageEnum, TTSModelParams] = {
            LanguageEnum.RU: TTSModelParams(
                model_id=settings.tts.TTS_MODEL_ID_RU,
                speaker=settings.tts.TTS_SPEAKER_RU,
            ),
            LanguageEnum.EN: TTSModelParams(
                model_id=settings.tts.TTS_MODEL_ID_EN,
                speaker=settings.tts.TTS_SPEAKER_EN,
            ),
        }
        self.DirPath = RepoDirConsts.PATH
