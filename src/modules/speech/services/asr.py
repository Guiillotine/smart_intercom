import logging

from fastapi import UploadFile
from faster_whisper import WhisperModel

from src.common.constants.enums import LanguageEnum
from src.common.decorators import LoggingFunctionInfo
from src.config.settings import Settings
from src.modules.speech.schemas import SpeechInfo


class ASRService(IASRService):
    def __init__(
        self,
        consts: ASRServiceConsts,
        logger: logging.Logger,
        settings: Settings,
        model: WhisperModel,
    ):
        self._consts = consts
        self._logger = logger
        self._model = model

        self._model = WhisperModel(
            model_size_or_path=settings.asr.ASR_MODEL_SIZE,
            device=settings.runtime.DEVICE,
            compute_type=settings.asr.ASR_COMPUTE_TYPE,
        )

    @LoggingFunctionInfo("Speech to text")
    def speech_to_text(
        self,
        audio: UploadFile,
        dialog_lang: LanguageEnum | None = None,
    ) -> SpeechInfo:
        segments, info = self._model.transcribe(audio, beam_size=4)

        if info.language not in LanguageEnum.get_all_langs():
            self._logger.warning("Couldn't recognize language.")
            lang = (
                dialog_lang
                if dialog_lang is not None
                else self._consts.Common.Language.DEFAULT_LANG
            )
        else:
            lang = LanguageEnum(info.language)

        text = " ".join(seg.text.strip() for seg in segments).strip()

        return SpeechInfo(
            lang=lang,
            text=text,
        )
