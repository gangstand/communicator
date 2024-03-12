from uuid import UUID

from litestar import Controller, Request, delete, get, patch, post

from app.repository import PermissionRepository
from app.schemas import PermissionCreate, PermissionRead, PermissionUpdate, pagination_generate
from domain.typing import EntityList, Response


class Permission(Controller):
    _permission_repository = PermissionRepository

    @get()
    async def get_permissions(
            self, request: Request,
            page: int = 1,
            offset: int = 50,
            is_removing: bool = False,
    ) -> pagination_generate(PermissionRead):
        params = {}
        return await self._permission_repository.get_all(request, page, offset, is_removing, params)

    @get("/{permission_id:uuid}")
    async def get_permission(self, permission_id: UUID, request: Request) -> PermissionRead:
        return await self._permission_repository.get_one(permission_id, request)

    @patch("/{permission_id:uuid}", status_code=201)
    async def update_permission(self, permission_id: UUID, data: PermissionUpdate, request: Request) -> PermissionRead:
        return await self._permission_repository.update(permission_id, data, request)

    @post(status_code=201)
    async def create_permission(self, data: PermissionCreate, request: Request) -> PermissionRead:
        return await self._permission_repository.create(data, request)

    @delete("/{permission_id:uuid}", status_code=201)
    async def delete_permission(self, permission_id: UUID, request: Request) -> Response:
        return await self._permission_repository.delete(permission_id, request)

    @patch("/soft_delete/{permission_id:uuid}", status_code=201)
    async def soft_delete_permission(self, permission_id: UUID, is_removing: bool, request: Request) -> Response:
        return await self._permission_repository.soft_delete(permission_id, request, is_removing)

    @patch("/soft_delete/batch", status_code=201)
    async def soft_delete_batch_permission(self, data: EntityList, is_removing: bool, request: Request) -> Response:
        return await self._permission_repository.soft_delete_batch(data, request, is_removing)
