from src.client.storages.deps import get_postgres_session_provider
from src.client.storages.postgres.core.deps import get_psql_session_context_manager
from src.common.constants.deps import get_error_codes_enums
from src.common.logger.constants.deps import get_logger_config
from src.common.logger.deps import get_base_logger, get_logger_manager
from src.config.settings.deps import get_settings
from src.server.middleware import BackendExceptionHandler
from src.server.middleware.exception import ValidationExceptionHandler, \
    ExceptionMiddleware, BotDialogueExceptionHandler
from src.server.middleware.psql_context_manager import PostgresContextSessionMiddleware


def get_exception_middleware() -> ExceptionMiddleware:
    """
    This function provides the middleware that handles any uncaught exceptions during
    the request-response cycle. It logs the exception and returns a default error
    response when an unhandled error occurs.

    :return: An instance of `ExceptionMiddleware`, which handles uncaught exceptions in
            FastAPI.
    """
    return ExceptionMiddleware(
        logger=get_base_logger(get_logger_manager(get_logger_config())),
        errors=get_error_codes_enums(),
    )


def get_backend_exception_handler() -> BackendExceptionHandler:
    return BackendExceptionHandler()


def get_validation_exception_handler() -> ValidationExceptionHandler:
    return ValidationExceptionHandler(
        logger=get_base_logger(get_logger_manager(get_logger_config())),
        errors=get_error_codes_enums(),
    )


def get_bot_dialogue_exception_handler() -> BotDialogueExceptionHandler:
    return BotDialogueExceptionHandler()


def get_postgres_context_session_middleware() -> PostgresContextSessionMiddleware:
    return PostgresContextSessionMiddleware(
        errors=get_error_codes_enums(),
        postgres_session_context_manager=get_psql_session_context_manager(),
        postgres_session_provider=get_postgres_session_provider(settings=get_settings())
    )
