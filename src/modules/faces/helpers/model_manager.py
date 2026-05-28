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
        )
        # Delete from pypeline extra stages
        self._app.prepare(
            ctx_id=-1,
            det_size=(640, 640),
            det_thresh=settings.face.DET_SCORE_THRESHOLD,
        )

    @property
    def app(self) -> FaceAnalysis:
        return self._app
