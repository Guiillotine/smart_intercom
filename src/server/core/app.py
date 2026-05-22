from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from faster_whisper import WhisperModel
from openai import OpenAI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.common.errors import BackendException
from src.config.docs.deps import get_tags_metadata
from src.config.settings.deps import get_settings
from src.modules.speech.handlers import TTSModelManager
from src.modules.speech.handlers.constants.deps import get_tts_model_manager_consts
from src.server.core.controllers import api_controller
from src.server.middleware.deps import get_backend_exception_handler, \
    get_postgres_context_session_middleware, get_exception_middleware, \
    get_validation_exception_handler

# === Constants === #
origins = [
    "*",
]

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_state()
    yield
    clean_state()


app = FastAPI(
    debug=settings.project.DEBUG,
    title=settings.project.PROJECT_NAME,
    version=settings.project.PROJECT_VERSION,
    lifespan=lifespan,
    openapi_tags=get_tags_metadata().get_tags_metadata(),
    exception_handlers={BackendException: get_backend_exception_handler().handle},
)


# === Middleware Setup === #
def setup_middleware():
    """
    Configures middleware for CORS and session handling.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        SessionMiddleware, # TODO: это что?
        secret_key=get_settings().project.SESSION_SECRET_KEY,
    )
    #app.middleware("http")(get_jwt_context_middleware())
    app.middleware("http")(get_exception_middleware())
    app.middleware("http")(get_postgres_context_session_middleware())

    app.exception_handler(RequestValidationError)(
        get_validation_exception_handler().handle,
    )


# === Router Setup === #
def include_routers():
    """
    Includes all application routes with API versioning.
    """
    app.include_router(api_controller, prefix=get_settings().project.API_V1_STR)


# === Initialize App Configuration === #
def initialize_app():
    """
    Calls all setup functions to configure the application.
    """
    setup_middleware()
    include_routers()


def initialize_state():
    app.state.whisper_model = WhisperModel(
        model_size_or_path=settings.asr.ASR_MODEL_SIZE,
        device=settings.runtime.DEVICE,
        compute_type=settings.asr.ASR_COMPUTE_TYPE,
    )
    app.state.tts_model_manager = TTSModelManager(
        consts=get_tts_model_manager_consts(settings),
    )
    app.state.client = OpenAI(
        api_key=settings.bot.API_KEY,
        base_url=settings.bot.BASE_URL,
        max_retries=settings.bot.LLM_HTTP_RETRIES,
        timeout=settings.bot.LLM_RESPONSE_TIMEOUT_SEC,
    )


def clean_state():
    del app.state.whisper_model
    del app.state.tts_model_manager
    del app.state.client


# === Run App Initialization === #
initialize_app()
