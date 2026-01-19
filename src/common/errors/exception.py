from enum import Enum

from fastapi import HTTPException


class BackendException(HTTPException):
    def __init__(self, error: Enum, cause: str = ""):

        self.error_code = error.value[0]
        self.status_code = error.value[1]
        self.detail = error.value[2]
        self.cause = cause
