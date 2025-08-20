from src.server.middleware import BackendExceptionHandler


def get_backend_exception_handler():
    return BackendExceptionHandler()
