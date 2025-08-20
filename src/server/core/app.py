from fastapi import FastAPI

from src.common.errors import BackendException
from src.config.docs.deps import get_tags_metadata
from src.config.settings.deps import get_settings
from src.server.middleware.deps import get_backend_exception_handler

settings = get_settings()

app = FastAPI(
    debug=settings.PROJECT.DEBUG,
    title=settings.PROJECT.PROJECT_NAME,
    version=settings.PROJECT.PROJECT_VERSION,
    openapi_tags=get_tags_metadata().get_tags_metadata(),
    exception_handlers={BackendException: get_backend_exception_handler().handle},
)
