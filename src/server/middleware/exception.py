from fastapi import Request
from starlette.responses import JSONResponse

from src.common.errors import BackendException


class BackendExceptionHandler:
    @staticmethod
    async def handle(_: Request, exc: BackendException) -> JSONResponse:
        content = {
            "code": exc.status_code,
            "detail": exc.detail,
            "cause": exc.cause,
        }

        return JSONResponse(content, status_code=exc.status_code)

# TODO: ExceptionHandler

# TODO: ValidationExceptionHandler
