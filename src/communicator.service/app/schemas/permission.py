from pydantic import BaseModel, Field

from domain.typing import EntityRead, OptionalString


class PermissionRead(EntityRead):
    name: str


class PermissionCreate(BaseModel):
    name: str


class PermissionUpdate(BaseModel):
    name: OptionalString = Field(None)
