import logging
from time import perf_counter

from fastapi import UploadFile
from faster_whisper import WhisperModel

from src.common.constants.enums import LanguageEnum
from src.common.decorators import LoggingFunctionInfo
from src.config.settings import Settings
from src.modules.speech.interfaces import IASRSrv
from src.modules.speech.schemas import SpeechInfo
from src.modules.speech.services.constants import ASRServiceConsts


class ASRSrv(IASRSrv):
    def __init__(
        self,
        consts: ASRServiceConsts,
        logger: logging.Logger,
        model: WhisperModel,
    ):
        self._consts = consts
        self._logger = logger
        self._model = model

    @LoggingFunctionInfo("Recognize text from audio.")
    def speech_to_text(
        self,
        audio: UploadFile,
        dialogue_lang: LanguageEnum | None = None,
    ) -> SpeechInfo:
        started_at = perf_counter()
        segments, info = self._model.transcribe(audio.file, beam_size=4)

        if info.language not in LanguageEnum.get_all_langs():
            self._logger.warning("Couldn't recognize language.")
            lang = (
                dialogue_lang
                if dialogue_lang is not None
                else self._consts.Common.DefaultLanguage
            )
        else:
            lang = LanguageEnum(info.language)

        text = " ".join(seg.text.strip() for seg in segments).strip()
        self._logger.info(
            "[perf] speech_to_text_ms=%.2f lang=%s text_chars=%d",
            self._elapsed_ms(started_at),
            lang,
            len(text),
        )

        return SpeechInfo(
            lang=lang,
            text=text,
        )

    @staticmethod
    def _elapsed_ms(started_at: float) -> float:
        return (perf_counter() - started_at) * 1000
