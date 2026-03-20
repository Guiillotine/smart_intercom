from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TTSSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf8",
        extra="allow"
    )

    DEVICE: str = Field(default="cpu")

    TTS_MODEL_ID_RU: str = Field(default='v5_ru')

    TTS_SPEAKER_RU: str = Field(default='xenia')

    TTS_MODEL_ID_EN: str = Field(default='v3_en')

    TTS_SPEAKER_EN: str = Field(default='en_0')

    TTS_SAMPLE_RATE: int = Field(default=48000)
