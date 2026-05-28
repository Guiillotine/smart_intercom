import sys
from typing import ClassVar, TypeVar
import torch
from fastapi import Path

from src.common.constants.enums import LanguageEnum
from src.modules.speech.helpers.constants.consts import TTSModelManagerConsts
from src.modules.speech.helpers.protocols import SileroTTSProtocol
from src.modules.speech.interfaces import ITTSModelManager
from src.modules.speech.schemas import TTSModelParams


class TTSModelManager(ITTSModelManager[SileroTTSProtocol]):
    def __init__(
        self,
        consts: TTSModelManagerConsts,
    ):
        self._models = {}
        self._consts = consts

        repo_dir = str(self._consts.DirPath)

        for lang in LanguageEnum:
            params = self._consts.LangTTSModelMap[lang]

            if not params:
              print("Отсутствуют параметры модели для языка:", lang)
              raise Exception

            model, _ = torch.hub.load(
                repo_or_dir=repo_dir,
                model="silero_tts",
                language=lang.value,
                speaker=params.model_id,
                source="local",
            )

            self._models[lang] = model

    def get_model(self, lang: LanguageEnum) -> tuple[SileroTTSProtocol, TTSModelParams]:
        return self._models[lang], self._consts.LangTTSModelMap[lang]
