from fastapi.security import OAuth2PasswordBearer

from src.config.settings.deps import get_settings

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=get_settings().project.API_V1_STR + "/auth/login",
    auto_error=False,
)
