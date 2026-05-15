from typing import Annotated

from fastapi import Depends

from src.config.settings import Settings
from src.config.settings.deps import get_settings
from src.modules.faces.helpers import FaceAnalysisModelManager
from src.modules.faces.interfaces import IFaceAnalysisModelManager


def get_face_analysis_model_manager(
    settings: Annotated[Settings, Depends(get_settings())]
) -> IFaceAnalysisModelManager:
    return FaceAnalysisModelManager(settings=settings)
