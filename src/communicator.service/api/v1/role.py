from uuid import UUID

from litestar import Controller, Request, delete, get, patch, post

from app.repository import RoleRepository
from app.schemas import RoleCreate, RoleRead, RoleUpdate, pagination_generate
from domain.typing import EntityList, Response


class Role(Controller):
    _role_repository = RoleRepository

    @get()
    async def get_roles(
            self, request: Request,
            page: int = 1,
            offset: int = 50,
            is_removing: bool = False,
    ) -> pagination_generate(RoleRead):
        params = {}
        return await self._role_repository.get_all(request, page, offset, is_removing, params)

    @get("/{role_id:uuid}")
    async def get_role(self, role_id: UUID, request: Request) -> RoleRead:
        return await self._role_repository.get_one(role_id, request)

    @patch("/{role_id:uuid}", status_code=201)
    async def update_role(self, role_id: UUID, data: RoleUpdate, request: Request) -> RoleRead:
        return await self._role_repository.update(role_id, data, request)

    @post(status_code=201)
    async def create_role(self, data: RoleCreate, request: Request) -> RoleRead:
        return await self._role_repository.create(data, request)

    @delete("/{role_id:uuid}", status_code=201)
    async def delete_role(self, role_id: UUID, request: Request) -> Response:
        return await self._role_repository.delete(role_id, request)

    @patch("/soft_delete/{role_id:uuid}", status_code=201)
    async def soft_delete_role(self, role_id: UUID, is_removing: bool, request: Request) -> Response:
        return await self._role_repository.soft_delete(role_id, request, is_removing)

    @patch("/soft_delete/batch", status_code=201)
    async def soft_delete_batch_role(self, data: EntityList, is_removing: bool, request: Request) -> Response:
        return await self._role_repository.soft_delete_batch(data, request, is_removing)
