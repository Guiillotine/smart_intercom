import io
from logging import Logger

import soundfile as sf

from src.common.constants.enums import LanguageEnum
from src.config.settings import Settings
from src.modules.speech.handlers import TTSModelManager
from src.modules.speech.interfaces import ITTSService, ISpeechS3Repo
from src.modules.speech.schemas import AudioData


class TTSService(ITTSService):
    def __init__(
        self,
        logger: Logger,
        settings: Settings,
        tts_model_manager: TTSModelManager,
    ):
        self._logger = logger
        self._settings = settings
        self._tts_model_manager = tts_model_manager

    async def synthesize(self, text: str, lang: LanguageEnum=LanguageEnum.RU) -> AudioData:
        model, params = self._tts_model_manager.get_model(lang=lang)
        print(type(model), type(params))

        audio = model.apply_tts( # TODO: добавить в протокол
            text=text,
            speaker=params.speaker,
            sample_rate=self._settings.tts.TTS_SAMPLE_RATE,
        )

        buffer = io.BytesIO()

        sf.write(
            file=buffer,
            data=audio.cpu().numpy(),
            samplerate=self._settings.tts.TTS_SAMPLE_RATE,
            format="WAV",
        )

        return AudioData(
            data=buffer.getvalue(),
            content_type="audio/wav",
        )
