from abc import ABC, abstractmethod

from fastapi import APIRouter


class IIntercomController(ABC):
    @property
    @abstractmethod
    def controller(self) -> APIRouter:
        pass
