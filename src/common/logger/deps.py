import logging
from typing import Annotated

from fastapi import Depends

from src.common.logger import LoggerManager
from src.common.logger.constants import LoggerConfigEnums
from src.common.logger.constants.deps import get_logger_config


def get_logger_manager(
    config_enums: Annotated[LoggerConfigEnums, Depends(get_logger_config)],
) -> LoggerManager:
    return LoggerManager(config=config_enums)


def get_base_logger(
    logger_manager: Annotated[LoggerManager, Depends(get_logger_manager)]
) -> logging.Logger:
    return logger_manager.get_base_logger()


def get_visit_logger(
    logger_manager: Annotated[LoggerManager, Depends(get_logger_manager)]
) -> logging.Logger:
    return logger_manager.get_visit_logger()


def get_person_logger(
    logger_manager: Annotated[LoggerManager, Depends(get_logger_manager)]
) -> logging.Logger:
    return logger_manager.get_person_logger()


def get_message_logger(
    logger_manager: Annotated[LoggerManager, Depends(get_logger_manager)]
) -> logging.Logger:
    return logger_manager.get_message_logger()


def get_user_logger(
    logger_manager: Annotated[LoggerManager, Depends(get_logger_manager)]
) -> logging.Logger:
    return logger_manager.get_user_logger()


def get_face_logger(
    logger_manager: Annotated[LoggerManager, Depends(get_logger_manager)]
) -> logging.Logger:
    return logger_manager.get_face_logger()


def get_speech_logger(
    logger_manager: Annotated[LoggerManager, Depends(get_logger_manager)]
) -> logging.Logger:
    return logger_manager.get_speech_logger()


def get_dialogue_logger(
    logger_manager: Annotated[LoggerManager, Depends(get_logger_manager)]
) -> logging.Logger:
    return logger_manager.get_dialogue_logger()

