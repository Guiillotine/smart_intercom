import logging
from abc import ABC, abstractmethod


class ILoggerManager(ABC):
    """
    Interface for a logger manager that provides access to various
    loggers used throughout the application.

    Each logger should be configured according to the project’s
    logging standards (level, format, handlers, etc.).
    """

    @abstractmethod
    def get_base_logger(self) -> logging.Logger:
        """Returns the base application logger (general-purpose logging)."""
        ...

    @abstractmethod
    def get_visit_logger(self) -> logging.Logger:
        """Get logger for visit-specific application logs."""
        ...

    @abstractmethod
    def get_person_logger(self) -> logging.Logger:
        """Get logger for person-specific application logs."""
        ...

    @abstractmethod
    def get_message_logger(self) -> logging.Logger:
        """Get logger for message-specific application logs."""
        ...

    @abstractmethod
    def get_user_logger(self) -> logging.Logger:
        """Get logger for user-specific application logs."""
        ...

    @abstractmethod
    def get_face_logger(self) -> logging.Logger:
        """Get logger for face-specific application logs."""
        ...

    @abstractmethod
    def get_speech_logger(self) -> logging.Logger:
        """Get logger for speech-specific application logs."""
        ...

    @abstractmethod
    def get_dialogue_logger(self) -> logging.Logger:
        """Get logger for dialogue-specific application logs."""
        ...
