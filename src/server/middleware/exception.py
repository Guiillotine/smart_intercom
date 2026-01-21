import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from src.common.constants import ErrorCodesEnums
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


class ValidationExceptionHandler:
    """
    Handles validation errors, such as those caused by RequestValidationError.

    This class formats the validation exception into a structured JSON response,
    including error details and additional validation error data.
    """

    def __init__(
        self,
        logger: logging.Logger,
        errors: ErrorCodesEnums,
    ):
        """
        Initialize the validation exception handler with a logger and error codes.

        :param logger: The logger used for logging validation errors.
        :param errors: An instance of ErrorCodesEnums to retrieve error codes.
        """

        self._logger = logger
        self._errors = errors

    async def handle(
        self,
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        """
        Handle validation exception and format the error response.

        :param request: The HTTP request that caused the validation error.
        :param exc: The RequestValidationError to handle.
        :return: A JSONResponse with validation error details and additional data.
        """

        unprocessable_entity_error = BackendException(
            self._errors.Common.UNPROCESSABLE_ENTITY,
        )
        exc_str = f"{exc}".replace("   ", " ")
        self._logger.error(f"{request}: {exc_str}") # TODO: см
        content = {
            "status_code": unprocessable_entity_error.status_code,
            "message": unprocessable_entity_error.description,
            "data": exc.__dict__.get("_errors", []),
        }
        return JSONResponse(
            content=content,
            status_code=unprocessable_entity_error.status_code,
        )
