from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.models.entity import Entity


class Role(Entity):
    __tablename__ = "role"

    name: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    users: Mapped[list["User"]] = relationship(
        "User", secondary="associative_user_role", overlaps="roles",
    )
    permissions: Mapped[list["Permission"]] = relationship(
        "Permission", secondary="associative_role_permission", lazy="subquery",
    )
