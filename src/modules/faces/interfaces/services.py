from abc import abstractmethod, ABC

import numpy as np
from fastapi import UploadFile

from src.modules.faces.schemas import FaceInfo


class IFaceAnalyzerSrv(ABC):
    """
    Interface for face analyzer service.

    Defines the contract for services that detect faces in an image and extract
    face-related metadata, including detected age, sex, cropped face photo path,
    and normalized face embedding.
    """

    @abstractmethod
    async def analyse_photo(
        self,
        image: np.ndarray | UploadFile,
    ) -> list[FaceInfo]:
        """
        Analyze an image and return information about all detected faces.

        The method detects faces in the provided image, normalizes detected face
        bounding boxes to image bounds, extracts face crops, normalizes face
        embeddings, and returns structured face information.

        :param image: Input image as a NumPy array.
        :return: List of detected faces with age, sex, cropped photo path and
                normalized face embedding.
        """
        ...
