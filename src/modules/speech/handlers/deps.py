from src.modules.speech.handlers import TTSModelManager
from fastapi import Request


def get_tts_model_manager(request: Request) -> TTSModelManager:
    return request.app.state.tts_model_manager