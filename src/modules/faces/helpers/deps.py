from fastapi import Request

from src.modules.faces.interfaces import IFaceAnalysisModelManager


def get_face_analysis_model_manager(request: Request) -> IFaceAnalysisModelManager:
    return request.app.state.face_analysis_model_manager
