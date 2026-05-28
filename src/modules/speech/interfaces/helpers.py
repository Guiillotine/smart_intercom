from __future__ import annotations

from typing import TypeVar
import torch
from abc import ABC, abstractmethod

from src.common.constants.enums import LanguageEnum
from src.modules.speech.schemas import TTSModelParams

TTSModelType = TypeVar("TTSModelType")


class ITTSModelManager[TTSModelType](ABC):
    """
    Interface for TTS model manager operations.

    Defines model lookup contract for text-to-speech synthesis.
    """

    @abstractmethod
    def get_model(self, lang: LanguageEnum) -> tuple[TTSModelType, TTSModelParams]:
        """
        Get TTS model and parameters by language.

        :param lang: Requested synthesis language.
        :return: TTS model instance and its parameters.
        """
        ...
