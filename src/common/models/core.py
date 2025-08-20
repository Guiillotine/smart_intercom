from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class CoreModel(DeclarativeBase):
    # TODO: created_at, updated_at

    @classmethod
    @declared_attr
    def __tablename__(cls):
        name = cls.__name__.replace("Model", "")
        snake_case_name = [name[0].lower()]
        for c in name[1:]:
            snake_case_name.append("_" + c.lower() if c.isupper() else c)

        return "".join(snake_case_name)
