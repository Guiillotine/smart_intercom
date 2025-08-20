from fastapi import HTTPException

from src.common.constants import ErrorCodesEnums


class BackendException(HTTPException):
    def __init__(self, error: ErrorCodesEnums, cause: str = ""):
        self.error_code = error.value[0]
        self.status_code = error.value[1]
        self.detail = error.value[2]
        self.cause = cause
