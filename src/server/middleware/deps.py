from src.client.storages.deps import get_postgres_session_provider
from src.client.storages.postgres.core.deps import get_psql_session_context_manager
from src.common.constants.deps import get_error_codes_enums
from src.config.settings.deps import get_settings
from src.server.middleware import BackendExceptionHandler
from src.server.middleware.exception import ValidationExceptionHandler
from src.server.middleware.psql_context_manager import PostgresContextSessionMiddleware


def get_backend_exception_handler():
    return BackendExceptionHandler()

# TODO
#def get_exception_middleware() -> IExceptionMiddleware:
#    return ExceptionMiddleware(
#        logger=get_base_logger(get_logger_manager(get_logger_config())),
#        errors=get_error_codes(),
#    )


def get_validation_exception_handler() -> ValidationExceptionHandler:
    return ValidationExceptionHandler(
        logger=get_base_logger(get_logger_manager(get_logger_config())),
        errors=get_error_codes_enums(),
    )


def get_postgres_context_session_middleware() -> PostgresContextSessionMiddleware:
    return PostgresContextSessionMiddleware(
        errors=get_error_codes_enums(),
        postgres_session_context_manager=get_psql_session_context_manager(),
        postgres_session_provider=get_postgres_session_provider(settings=get_settings())
    )


#def get_jwt_context_middleware() -> IJWTContextMiddleware:
#    return JWTContextMiddleware()
