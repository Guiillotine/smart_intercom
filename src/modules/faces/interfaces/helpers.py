from abc import ABC, abstractmethod

from insightface.app import FaceAnalysis


class IFaceAnalysisModelManager(ABC):

    @property
    @abstractmethod
    def app(self) -> FaceAnalysis:
        ...
