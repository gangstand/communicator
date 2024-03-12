from uuid import UUID

from litestar import Controller, Request, delete, get, patch, post

from app.repository import UserRepository
from app.schemas import UserCreate, UserRead, UserUpdate, pagination_generate
from domain.typing import EntityList, Response


class User(Controller):
    _user_repository = UserRepository

    @get()
    async def get_users(
            self, request: Request,
            page: int = 1,
            offset: int = 50,
            is_removing: bool = False,
    ) -> pagination_generate(UserRead):
        params = {}
        return await self._user_repository.get_all(request, page, offset, is_removing, params)

    @get("/{user_id:uuid}")
    async def get_user(self, user_id: UUID, request: Request) -> UserRead:
        return await self._user_repository.get_one(user_id, request)

    @patch("/{user_id:uuid}", status_code=201)
    async def update_user(self, user_id: UUID, data: UserUpdate, request: Request) -> UserRead:
        return await self._user_repository.update(user_id, data, request)

    @post(status_code=201)
    async def create_user(self, data: UserCreate, request: Request) -> UserRead:
        return await self._user_repository.create(data, request)

    @delete("/{user_id:uuid}", status_code=201)
    async def delete_user(self, user_id: UUID, request: Request) -> Response:
        return await self._user_repository.delete(user_id, request)

    @patch("/soft_delete/{user_id:uuid}", status_code=201)
    async def soft_delete_user(self, user_id: UUID, is_removing: bool, request: Request) -> Response:
        return await self._user_repository.soft_delete(user_id, request, is_removing)

    @patch("/soft_delete/batch", status_code=201)
    async def soft_delete_batch_user(self, data: EntityList, is_removing: bool, request: Request) -> Response:
        return await self._user_repository.soft_delete_batch(data, request, is_removing)
