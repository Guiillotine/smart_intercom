from fastapi import Request
from openai import OpenAI


def get_openai_client(request: Request) -> OpenAI:
    return request.app.state.whisper_model
