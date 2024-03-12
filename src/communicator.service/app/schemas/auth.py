from pydantic import BaseModel, ConfigDict, Field

from app.schemas.role import RoleRead
from domain.typing import EntityIdRead, EntityRead, OptionalListEntityIdRead, OptionalString


class AuthUserRead(EntityRead):
    name: OptionalString
    email: str
    phone: str
    roles: list[RoleRead]
    chats: list[EntityIdRead]

    model_config = ConfigDict(from_attributes=True)


class AuthUserUpdate(BaseModel):
    name: OptionalString = Field(None)
    phone: OptionalString = Field(None)
    email: OptionalString = Field(None)
    chats: OptionalListEntityIdRead = Field(None)
    roles: OptionalListEntityIdRead = Field(None)


class AuthUserCreate(BaseModel):
    name: OptionalString = Field(None)
    email: str
    password: str
    phone: str
    chats: OptionalListEntityIdRead = Field(None)


class AuthUserPasswordUpdate(BaseModel):
    token: str
    password: str


class AuthUserLogin(BaseModel):
    email: str
    password: str


class AuthUserPhoneLogin(BaseModel):
    phone: str
    password: str


class LoginResponse(BaseModel):
    access: str
    refresh: str


class RefreshResponse(BaseModel):
    refresh: str


class Recovery(BaseModel):
    email: str
