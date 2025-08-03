from fastapi import FastAPI

from app.config import settings, docs_metadata

app = FastAPI(
    debug=settings.PROJECT.DEBUG,
    title=settings.PROJECT.PROJECT_NAME,
    version=settings.PROJECT.PROJECT_VERSION,
    openapi_tags=docs_metadata
)