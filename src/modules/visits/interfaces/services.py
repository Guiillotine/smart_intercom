from abc import ABC, abstractmethod
from uuid import UUID
from typing import TYPE_CHECKING

from fastapi import UploadFile

from src.common.constants.srv_req_enums import VisitRequirementsEnum
from src.common.schemas import ListResult, Msg, Pagination, PaginationResult, SortBase
from src.modules.visits.constants.enums import VisitHandoffReasonEnum, \
    VisitFinishReasonEnum
from src.modules.visits.filters.visit import VisitFilterFull
from src.modules.visits.schemas import (
    Visit,
    VisitCreate,
    VisitReport,
    VisitUpdate, VisitPersonCreate, VisitPerson, VisitPhotoResponse,
)
if TYPE_CHECKING:
    from src.modules.visits.services.constants.consts import VisitRespSchemas


class IVisitSrv(ABC):
    """
    Interface for visit service operations.

    Defines business operations for visit state management.
    """
    @abstractmethod
    async def get_by_sid(
        self,
        sid: UUID,
        requirement: VisitRequirementsEnum | None = None,
    ) -> "VisitRespSchemas.GET_BY_SID":
        """
        Get visit by identifier.

        :param sid: Visit identifier.
        :param requirement: Requirements for response schema.
        :return: Visit data.
        """
        ...

    @abstractmethod
    async def get_all(
        self,
        filters: VisitFilterFull | None = None,
        sort_params: SortBase | None = None,
        requirement: VisitRequirementsEnum | None = None,
    ) -> ListResult["VisitRespSchemas.GET_ALL"]:
        """
        Get all visits.

        :param filters: Optional filter schema.
        :param sort_params: Optional sorting parameters.
        :param requirement: Requirements for response schema.
        :return: Paginated visit list.
        """
        ...

    @abstractmethod
    async def get_all_paginated(
        self,
        pagination_params: Pagination,
        filters: VisitFilterFull = None,
        sort_params: SortBase = None
    ) -> PaginationResult[Visit]:
        """
        Get paginated visits.

        :param pagination_params: Pagination parameters.
        :param filters: Optional filter schema.
        :param sort_params: Optional sorting parameters.
        :return: Paginated visit list.
        """
        ...

    @abstractmethod
    async def get_waiting_decision_visits(self) -> ListResult[VisitReport]:
        """
        Get visits waiting for a door opening decision.

        :return: List of visit reports.
        """
        ...

    @abstractmethod
    async def create_visit(self, visit_in: VisitCreate) -> Visit:
        """
        Create a visit.

        :param visit_in: Visit creation schema.
        :return: Created visit.
        """
        ...

    @abstractmethod
    async def create_visitor(self, visit_person_in: VisitPersonCreate) -> VisitPerson:
        """
        Create a visitor.

        :param visit_person_in: Visitor creation schema.
        :return: Created visitor.
        """
        ...

    @abstractmethod
    async def save_visit_photo(
        self,
        sid: UUID,
        photo: UploadFile,
    ) -> VisitPhotoResponse:
        """
        Upload visit photo
        :param sid: Visit identifier.
        :param photo: Upload photo data.
        :return: Visit photo path.
        """
        ...

    @abstractmethod
    async def update_visit(self, sid: UUID, visit_in: VisitUpdate) -> Visit:
        """
        Update a visit.

        :param sid: Visit identifier.
        :param visit_in: Visit update schema.
        :return: Updated visit.
        """
        ...

    @abstractmethod
    async def call_employee(
        self,
        sid: UUID,
        reason: VisitHandoffReasonEnum,
    ) -> Visit:
        """
        Move visit to employee decision state.

        :param sid: Visit identifier.
        :param reason: Call employee reason.
        :return: Updated visit.
        """
        ...

    @abstractmethod
    async def ask_want_to_enter(
        self,
        sid: UUID,
    ) -> Visit:
        """
        Set visit status to 'asked wanted to enter'.

        :param sid: Visit identifier.
        :return: Updated visit.
        """
        ...

    @abstractmethod
    async def finish_visit(
        self,
        sid: UUID,
        finish_reason: VisitFinishReasonEnum,
    ) -> Visit:
        """
        Finish a visit.

        :param sid: Visit identifier.
        :param finish_reason: Why visit was finished.
        :return: Updated visit.
        """
        ...

    @abstractmethod
    async def make_door_open_decision(
        self, sid: UUID, user_sid: UUID, door_open: bool
    ) -> Msg:
        """
        Persist user door opening decision.

        :param sid: Visit identifier.
        :param user_sid: User who made the decision.
        :param door_open: Whether the door should be opened.
        :return: Operation result message.
        """
        ...

    @abstractmethod
    async def delete_visit(self, sid) -> Msg:
        """
        Delete visit by identifier.

        :param sid: Visit identifier.
        :return: Operation result message.
        """
        ...
