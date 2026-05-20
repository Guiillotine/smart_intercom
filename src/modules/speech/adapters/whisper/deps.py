from fastapi import Request
from faster_whisper import WhisperModel


def get_whisper_model(request: Request) -> WhisperModel:
    return request.app.state.whisper_model
