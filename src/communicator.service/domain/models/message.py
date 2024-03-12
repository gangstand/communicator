from typing import Any
from uuid import UUID

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.models.chat import Chat
from domain.models.entity import Entity


class Message(Entity):
    __tablename__ = "message"

    data: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    type: Mapped[str]
    chat_id: Mapped[UUID] = mapped_column(ForeignKey("chat.id", ondelete="CASCADE"), nullable=False)
    chat: Mapped[Chat] = relationship(Chat, back_populates="messages", foreign_keys=[chat_id])
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="messages", foreign_keys=[user_id])



