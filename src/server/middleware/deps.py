from src.client.storages.deps import get_postgres_session_provider
from src.server.middleware import BackendExceptionHandler
from src.server.middleware.psql_context_manager import PostgresContextSessionMiddleware


def get_backend_exception_handler():
    return BackendExceptionHandler()

# TODO
#def get_exception_middleware() -> IExceptionMiddleware:
#    return ExceptionMiddleware(
#        logger=get_base_logger(get_logger_manager(get_logger_config())),
#        errors=get_error_codes(),
#    )


#def get_validation_exception_handler() -> IValidationExceptionHandler:
#    return ValidationExceptionHandler(
#        logger=get_base_logger(get_logger_manager(get_logger_config())),
#        errors=get_error_codes(),
#    )


def get_postgres_context_session_middleware() -> PostgresContextSessionMiddleware:
    return PostgresContextSessionMiddleware(
        errors=get_error_codes(),
        postgres_session_provider=get_postgres_session_provider(),
        postgres_session_context_manager=get_postgres_session_context_manager(),
    )


def get_jwt_context_middleware() -> IJWTContextMiddleware:
    # TODO: docs/comments
    return JWTContextMiddleware()
