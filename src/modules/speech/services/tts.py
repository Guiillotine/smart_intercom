from uuid import uuid4

from src.common.constants.enums import LanguageEnum
from src.config.settings import Settings
from src.modules.speech.handlers import TTSModelManager
from src.modules.speech.interfaces import ITTSService
from src.modules.speech.schemas import AudioData


class TTSService(ITTSService):
    def __init__(
        self,
        settings: Settings,
        tts_model_manager: TTSModelManager,
    ):
        self._settings = settings
        self._tts_model_manager = tts_model_manager
        self._speech_s3_repo = SpeechS3Repo

    def synthesize(self, text: str, lang: LanguageEnum=LanguageEnum.RU) -> AudioData:
        model, params = self._tts_model_manager.get_model(lang=lang)
        print(type(model), type(params))

        audio = model.apply_tts(
            text=text,
            speaker=params.speaker,
            sample_rate=self._settings.tts.TTS_SAMPLE_RATE,
        )

        print("\nMADE AUDIO FROM TEXT:", text)

        id = uuid4() # TODO: тестовая заглушка

        s3_path = self._speech_s3_repo.put_object(
            name=f"output_{lang.value}_{id}.mp3",
            audio=audio,
            tts_sample_rate=self._settings.tts.TTS_SAMPLE_RATE,
        )

        return AudioData(
            s3_path=s3_path
        )
