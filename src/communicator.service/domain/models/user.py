from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.models.chat import Chat
from domain.models.entity import Entity
from domain.models.message import Message
from domain.models.role import Role


class User(Entity):
    __tablename__ = "user"

    name: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    roles: Mapped[list[Role]] = relationship(
        "Role", secondary="associative_user_role", lazy=False,
    )
    chats: Mapped[list[Chat]] = relationship(
        "Chat", secondary="associative_user_chat", lazy=False,
    )
    messages: Mapped[list[Message]] = relationship("Message", back_populates="user")
