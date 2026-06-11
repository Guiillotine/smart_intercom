from pydantic import Field
from pydantic_settings import BaseSettings


class SchedulerSettings(BaseSettings):
    # VISIT
    CALL_EMPLOYEE_TIMEOUT_SEC: int | None = Field(
        default=300, description="Visit in WAITING_DECISION status finish sec"
    )
