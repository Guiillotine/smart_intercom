from dataclasses import dataclass
from enum import Enum, StrEnum

from src.config.settings.deps import get_settings


@dataclass(frozen=True)
class LoggerConfig:
    name: str
    level: str
    format: str


class LoggerNameEnum(StrEnum):
    """Predefined logger names."""

    BASE = "BASE"
    VISIT = "VISIT"
    PERSON = "PERSON"
    MESSAGE = "MESSAGE"
    USER = "USER"
    FACE = "FACE"


class LoggerLevelEnum(StrEnum):
    """Defines the available log levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LoggerFormatEnum(StrEnum):
    """Defines different formats for logging."""

    BASE = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) %(message)s"


class LoggerConfigEnum(Enum):
    """Centralized container for logger configuration presets."""

    BASE = LoggerConfig(
        LoggerNameEnum.BASE,
        get_settings().project.LOG_LEVEL.upper(),
        LoggerFormatEnum.BASE,
    )
    VISIT = LoggerConfig(
        LoggerNameEnum.VISIT,
        get_settings().project.LOG_LEVEL.upper(),
        LoggerFormatEnum.BASE,
    )
    PERSON = LoggerConfig(
        LoggerNameEnum.PERSON,
        get_settings().project.LOG_LEVEL.upper(),
        LoggerFormatEnum.BASE,
    )
    MESSAGE = LoggerConfig(
        LoggerNameEnum.MESSAGE,
        get_settings().project.LOG_LEVEL.upper(),
        LoggerFormatEnum.BASE,
    )
    USER = LoggerConfig(
        LoggerNameEnum.USER,
        get_settings().project.LOG_LEVEL.upper(),
        LoggerFormatEnum.BASE,
    )
    FACE = LoggerConfig(
        LoggerNameEnum.FACE,
        get_settings().project.LOG_LEVEL.upper(),
        LoggerFormatEnum.BASE,
    )


class LoggerConfigEnums:
    """
    Centralized container for all grouped logger-related enums.
    """

    Format: type[LoggerFormatEnum] = LoggerFormatEnum
    Level: type[LoggerLevelEnum] = LoggerLevelEnum
    Name: type[LoggerNameEnum] = LoggerNameEnum
    Config: type[LoggerConfigEnum] = LoggerConfigEnum
