import io
from logging import Logger
from time import perf_counter

import soundfile as sf

from src.common.constants.enums import LanguageEnum
from src.common.decorators import LoggingFunctionInfo
from src.config.settings import Settings
from src.modules.speech.helpers import TTSModelManager
from src.modules.speech.interfaces import ITTSSrv, ISpeechS3Repo
from src.modules.speech.schemas import AudioData


class TTSSrv(ITTSSrv):
    def __init__(
        self,
        logger: Logger,
        settings: Settings,
        tts_model_manager: TTSModelManager,
    ):
        self._logger = logger
        self._settings = settings
        self._tts_model_manager = tts_model_manager

    @LoggingFunctionInfo("Synthesize speech from text.")
    def synthesize(self, text: str, lang: LanguageEnum=LanguageEnum.RU) -> AudioData:
        started_at = perf_counter()
        model, params = self._tts_model_manager.get_model(lang=lang)

        audio = model.apply_tts(
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

        audio_data = AudioData(
            data=buffer.getvalue(),
            content_type="audio/wav",
        )
        self._logger.info(
            "[PERF] tts_ms=%.2f", self._elapsed_ms(started_at),
        )
        return audio_data

    @staticmethod
    def _elapsed_ms(started_at: float) -> float:
        return (perf_counter() - started_at) * 1000
