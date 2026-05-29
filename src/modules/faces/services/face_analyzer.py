import logging
from asyncio import to_thread

import cv2
import numpy as np
from starlette.datastructures import UploadFile
from insightface.app.common import Face

from src.common.constants import ErrorCodesEnums
from src.common.decorators import LoggingFunctionInfo
from src.modules.faces.interfaces import IFaceAnalyzerSrv, IFaceAnalysisModelManager
from src.modules.faces.schemas import FaceInfo
from src.modules.faces.services.constants import FaceAnalyzerSrvEnums


class FaceAnalyzerSrv(IFaceAnalyzerSrv):
    """
    Face analyzer service.

    Provides methods for face analysis.
    """

    def __init__(
        self,
        logger: logging.Logger,
        enums: FaceAnalyzerSrvEnums,
        errors: ErrorCodesEnums,
        face_analysis_model_manager: IFaceAnalysisModelManager,
    ):
        self._logger = logger
        self._enums = enums
        self._errors = errors
        self._app = face_analysis_model_manager.app

    @LoggingFunctionInfo(
        description="Analyze an image and return information about all detected faces."
    )
    async def analyse_photo(
        self,
        image: np.ndarray | UploadFile,
    ) -> list[FaceInfo]:
        if isinstance(image, UploadFile):
            image = await self._upload_file_to_ndarray(image)

        faces = await to_thread(self._app.get, image)

        h, w = image.shape[:2]

        self._clamp_bbox_coords_to_bounds(y_bound=h, x_bound=w, faces=faces)

        faces_info: list[FaceInfo] = []
        for face in faces:
            face_embedding = self._l2_norm_embedding(embedding=face.embedding)
            x1, y1, x2, y2 = face.bbox

            faces_info.append(
                FaceInfo(
                    detected_age=getattr(face, "age", None),
                    detected_sex=(
                        self._enums.Common.Gender(face.gender)
                        if getattr(face, "gender", None) is not None
                        else None
                    ),
                    face_embedding=face_embedding,
                    crop_coords=[y1, y2, x1, x2],
                )
            )

        return faces_info

    def _clamp_bbox_coords_to_bounds(
        self,
        y_bound: int,
        x_bound: int,
        faces: list[Face],
    ) -> None:
        for face in faces:
            x1, y1, x2, y2 = map(int, face.bbox)

            x1 = max(0, min(x1, x_bound - 1))
            x2 = max(0, min(x2, x_bound))
            y1 = max(0, min(y1, y_bound - 1))
            y2 = max(0, min(y2, y_bound))

            if x2 <= x1 or y2 <= y1:
                self._logger.warning(msg=f"Skip invalid bbox: {face.bbox}")
                continue

            face.bbox = np.array((x1, y1, x2, y2), dtype=np.int32)

    @staticmethod
    def _l2_norm_embedding(embedding: list[float]) -> list[float]:
        n = np.linalg.norm(embedding)

        normalized = embedding / n if n != 0 else embedding
        return normalized.astype(np.float32).tolist()

    @staticmethod
    def _get_vector_len(v: list[float]) -> float:
        return sum(x * x for x in v)**0.5

    @staticmethod
    async def _upload_file_to_ndarray(image: UploadFile) -> np.ndarray:
        content = await image.read()
        image_array = np.frombuffer(content, dtype=np.uint8)
        image_as_ndarray = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        if image_as_ndarray is None:
            raise ValueError("Can't decode image")

        await image.seek(0)
        return image_as_ndarray
