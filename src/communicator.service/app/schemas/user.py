from pydantic import BaseModel, ConfigDict, Field

from app.schemas.role import RoleRead
from domain.typing import EntityIdRead, EntityRead, OptionalListEntityIdRead, OptionalString


class UserRead(EntityRead):
    name: OptionalString
    email: str
    phone: str
    password: str
    roles: list[RoleRead]
    chats: list[EntityIdRead]

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    name: OptionalString
    email: str
    phone: str
    password: str
    roles: OptionalListEntityIdRead = Field(None)
    chats: OptionalListEntityIdRead = Field(None)


class UserUpdate(BaseModel):
    name: OptionalString = Field(None)
    phone: OptionalString = Field(None)
    email: OptionalString = Field(None)
    password: OptionalString = Field(None)
    roles: OptionalListEntityIdRead = Field(None)
    chats: OptionalListEntityIdRead = Field(None)
