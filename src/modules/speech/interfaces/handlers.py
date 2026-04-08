from __future__ import annotations

from typing import TypeVar
import torch
from abc import ABC

from src.common.constants.enums import LanguageEnum
from src.modules.speech.schemas import TTSModelParams

TTSModelType = TypeVar("TTSModelType")


class ITTSModelManager[TTSModelType](ABC):
    def get_model(self, lang: LanguageEnum) -> tuple[TTSModelType, TTSModelParams]:
        ...
