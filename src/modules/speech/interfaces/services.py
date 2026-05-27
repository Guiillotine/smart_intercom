from __future__ import annotations

from abc import ABC, abstractmethod

from fastapi import UploadFile

from src.common.constants.enums import LanguageEnum
from src.modules.speech.schemas import SpeechInfo


class ITTSSrv(ABC):
    """
    Interface for TTS service operations.

    Defines speech synthesis contract.
    """

    @abstractmethod
    def synthesize(self, text: str, lang: LanguageEnum):
        """
        Synthesize speech from text.

        :param text: Text to synthesize.
        :param lang: Synthesis language.
        :return: Synthesized audio metadata.
        """
        ...


class IASRSrv(ABC):

    @abstractmethod
    def speech_to_text(
        self,
        audio: UploadFile,
        dialogue_lang: LanguageEnum | None = None,
    ) -> SpeechInfo:
        """
        Recognize text from audio.

        :param audio: Audio to recognize.
        :param dialogue_lang: Optional param to specify the language manual.
        :return: Speech recognition metadata.
        """
        ...
