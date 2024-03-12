from sqlalchemy.orm import Mapped

from domain.models.entity import Entity


class File(Entity):
    __tablename__ = "file"

    name: Mapped[str]
    path: Mapped[str]
