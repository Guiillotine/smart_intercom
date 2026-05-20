from abc import ABC

from src.common.interfaces import IPostgresBaseRepo
from src.modules.visits.models import VisitModel, VisitPersonModel
from src.modules.visits.schemas import VisitCreate, VisitPersonCreate, VisitUpdate


class IVisitPostgresRepo(IPostgresBaseRepo[VisitModel, VisitCreate, VisitUpdate], ABC):
    """
    Interface for visit PostgreSQL repository operations.

    Extends base PostgreSQL repository with the visit model contract.
    """


class IVisitPersonPostgresRepo(
    IPostgresBaseRepo[VisitPersonModel, VisitPersonCreate, VisitPersonCreate], ABC
):
    """
    Interface for visit person PostgreSQL repository operations.

    Extends base PostgreSQL repository with the visit-person model contract.
    """
