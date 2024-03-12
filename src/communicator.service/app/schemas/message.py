from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from domain.typing import EntityRead, OptionalString, OptionalUUID


class MessageRead(EntityRead):
    data: dict
    type: Literal["text", "file", "img", "video"]
    chat_id: UUID
    user_id: UUID


class MessageCreate(BaseModel):
    data: dict | None = Field(None)
    type: Literal["text", "file", "img", "video"] | None = Field(None)
    chat_id: OptionalUUID = Field(None)


class MessageCreateEvent(BaseModel):
    data: dict | None = Field(None)
    type: Literal["text", "file", "img", "video"] | None = Field(None)
    chat_id: OptionalUUID = Field(None)
    user_id: OptionalUUID = Field(None)


class MessageUpdate(BaseModel):
    data: dict | None = Field(None)
    type: OptionalString = Field(None)
    chat_id: OptionalUUID = Field(None)
