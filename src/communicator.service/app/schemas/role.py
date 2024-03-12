from pydantic import BaseModel, ConfigDict, Field

from domain.typing import EntityRead, OptionalListEntityIdRead, OptionalString

from .permission import PermissionRead


class RoleRead(EntityRead):
    name: str


class RoleWithPermissionsRead(EntityRead):
    name: str
    permissions: list[PermissionRead]

    model_config = ConfigDict(from_attributes=True)


class RoleCreate(BaseModel):
    name: str
    permissions: OptionalListEntityIdRead = Field(None)


class RoleUpdate(BaseModel):
    name: OptionalString = Field(None)
    permissions: OptionalListEntityIdRead = Field(None)
