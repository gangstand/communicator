from sqlalchemy.orm import Mapped, relationship

from domain.models.entity import Entity


class Chat(Entity):
    __tablename__ = "chat"

    name: Mapped[str]
    users: Mapped[list["User"]] = relationship("User", secondary="associative_user_chat", overlaps="chats", lazy=False)
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="chat")



