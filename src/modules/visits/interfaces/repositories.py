from abc import ABC

from src.common.interfaces import IPostgresBaseRepo, IS3BaseRepo
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


class IVisitS3Repo(IS3BaseRepo, ABC):
    """
    Interface for a visit-specific S3 repository.

    Defines additional visit-related S3 operations beyond the basic S3 repository
    functionality.
    """
