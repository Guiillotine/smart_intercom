from uuid import UUID, uuid4

from pgvector.sqlalchemy import Vector
from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column

from src.common.models import CoreModel
from src.common.adapters.repositories.postgres.constants import SchemaNamesEnum
from src.common.utils import table_args
from src.config.settings.deps import get_settings

settings = get_settings()


class PersonModel(CoreModel):
    __table_args__ = (
        Index(
            "idx_person_face_embedding",
            "face_embedding",
            postgresql_using="hnsw",
            postgresql_ops={"face_embedding": "vector_cosine_ops"},
        ),
        table_args(schema=SchemaNamesEnum.PERSONS),
    )

    sid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    first_name: Mapped[str]

    last_name: Mapped[str]

    middle_name: Mapped[str | None] = mapped_column(nullable=True)

    photo_s3_path: Mapped[str] = mapped_column(comment="S3 path to person photo")

    face_embedding: Mapped[list[float]] = mapped_column(
        Vector(get_settings().postgres.DIMENSION)
    )

    person_type: Mapped[int] = mapped_column(index=True, comment="Employee or Visitor")

    is_archived: Mapped[bool] = mapped_column(default=False)
