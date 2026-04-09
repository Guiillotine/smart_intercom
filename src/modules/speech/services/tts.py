from logging import Logger
from uuid import uuid4

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
        speech_s3_repo: ISpeechS3Repo,
    ):
        self._logger = logger
        self._settings = settings
        self._tts_model_manager = tts_model_manager
        self._speech_s3_repo = speech_s3_repo

    async def synthesize(self, text: str, lang: LanguageEnum=LanguageEnum.RU) -> AudioData:
        model, params = self._tts_model_manager.get_model(lang=lang)
        print(type(model), type(params))

        audio = model.apply_tts( # TODO: добавить в протокол
            text=text,
            speaker=params.speaker,
            sample_rate=self._settings.tts.TTS_SAMPLE_RATE,
        )

        s3_path = await self._speech_s3_repo.put_audio_message(
            key=str(uuid4()), # TODO: тестовая заглушка
            data=audio,
        )

        return AudioData(
            s3_path=s3_path
        )
