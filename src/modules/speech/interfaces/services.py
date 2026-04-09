from __future__ import annotations

from abc import ABC, abstractmethod

from src.common.constants.enums import LanguageEnum


class ITTSService(ABC):

    @abstractmethod
    async def synthesize(self, text: str, lang: LanguageEnum):
        ...
