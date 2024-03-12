from uuid import UUID

from pydantic import BaseModel, Field

from domain.typing import EntityIdRead, EntityRead, OptionalListEntityIdRead, OptionalString


class ChatRead(EntityRead):
    name: str
    users: list[EntityIdRead]


class ChatCreate(BaseModel):
    name: OptionalString = Field(None)
    users: list[EntityIdRead]


class ChatUpdate(BaseModel):
    name: OptionalString = Field(None)
    users: OptionalListEntityIdRead = Field(None)


class MessageSearch(BaseModel):
    chat_id: UUID
