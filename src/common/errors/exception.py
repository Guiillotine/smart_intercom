from enum import Enum

from fastapi import HTTPException


class BackendException(HTTPException):
    def __init__(self, error: Enum, cause: str = ""):
        self._error = error
        self.error_code = error.value[0]
        self.status_code = error.value[1]
        self.detail = error.value[2]
        self.cause = cause


class BotDialogueException(BackendException):
    def __init__(self, error: Enum, audio_s3_path: str):
        super().__init__(error=error)
        self.audio_s3_path = audio_s3_path

    @classmethod
    def from_backend_exception(
        cls,
        exc: BackendException,
        audio_s3_path: str,
    ) -> "BotDialogueException":
        return cls(
            error=exc._error,
            audio_s3_path=audio_s3_path,
        )
