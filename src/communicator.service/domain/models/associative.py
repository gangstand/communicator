from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from domain.models.entity import Entity


class AssociativeUserRole(Entity):
    __tablename__ = "associative_user_role"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True, index=True,
                                          default=None, nullable=False)
    role_id: Mapped[UUID] = mapped_column(ForeignKey("role.id", ondelete="CASCADE"), primary_key=True, index=True,
                                          default=None, nullable=False)


class AssociativeRolePermission(Entity):
    __tablename__ = "associative_role_permission"

    role_id: Mapped[UUID] = mapped_column(ForeignKey("role.id", ondelete="CASCADE"), primary_key=True, index=True,
                                          default=None, nullable=False)
    permission_id: Mapped[UUID] = mapped_column(ForeignKey("permission.id", ondelete="CASCADE"), primary_key=True,
                                                index=True, default=None, nullable=False)


class AssociativeUserChatPermission(Entity):
    __tablename__ = "associative_user_chat"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True, index=True,
                                          default=None, nullable=False)
    chat_id: Mapped[UUID] = mapped_column(ForeignKey("chat.id", ondelete="CASCADE"), primary_key=True, index=True,
                                          default=None, nullable=False)
