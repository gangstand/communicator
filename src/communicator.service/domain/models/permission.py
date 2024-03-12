from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.models.entity import Entity
from domain.models.role import Role


class Permission(Entity):
    __tablename__ = "permission"

    name: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    roles: Mapped[list[Role]] = relationship(
        Role, secondary="associative_role_permission", overlaps="permissions",
    )
