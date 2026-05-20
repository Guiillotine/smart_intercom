from __future__ import annotations

from abc import ABC, abstractmethod

from src.common.constants.enums import LanguageEnum


class ITTSService(ABC):
    """
    Interface for TTS service operations.

    Defines speech synthesis contract.
    """

    @abstractmethod
    async def synthesize(self, text: str, lang: LanguageEnum):
        """
        Synthesize speech from text.

        :param text: Text to synthesize.
        :param lang: Synthesis language.
        :return: Synthesized audio metadata.
        """
        ...
