from src.config.settings.asr import ASRSettings
from src.config.settings.bot import BotSettings
from src.config.settings.face import FaceSettings
from src.config.settings.postgres import PostgresSettings
from src.config.settings.project import ProjectSettings
from src.config.settings.runtime import RuntimeSettings
from src.config.settings.tts import TTSSettings


class Settings:
    project = ProjectSettings()
    postgres = PostgresSettings()
    runtime = RuntimeSettings()
    face = FaceSettings()
    tts = TTSSettings()
    asr = ASRSettings()
    bot = BotSettings()
