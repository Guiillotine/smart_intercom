from __future__ import annotations

from abc import ABC, abstractmethod

from src.common.constants.enums import LanguageEnum


class ITTSService(ABC):

    @abstractmethod
    def synthesize(self, text: str, lang: LanguageEnum):
        ...
