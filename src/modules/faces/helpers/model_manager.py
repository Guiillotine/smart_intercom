from insightface.app import FaceAnalysis

from src.config.settings import Settings
from src.modules.faces.interfaces import IFaceAnalysisModelManager


class FaceAnalysisModelManager(IFaceAnalysisModelManager):
    def __init__(
        self,
        settings: Settings,
    ):
        self._app = FaceAnalysis(
            name=settings.face.FACE_ANALYZE_MODEL,
            providers=[settings.face.FACE_PROVIDER],
            allowed_modules=["detection", "recognition", "genderage"],
        )
        ctx_id = 0 if settings.face.FACE_PROVIDER == "CUDAExecutionProvider" else -1
        # Delete from pypeline extra stages
        self._app.prepare(
            ctx_id=ctx_id,
            det_size=(settings.face.FACE_DET_SIZE, settings.face.FACE_DET_SIZE),
            det_thresh=settings.face.DET_SCORE_THRESHOLD,
        )

    @property
    def app(self) -> FaceAnalysis:
        return self._app
