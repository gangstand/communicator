from __future__ import annotations

from typing import TYPE_CHECKING

from app.interfaces import IRepository
from app.schemas import UserCreate, UserRead, UserUpdate, pagination_generate
from domain import BaseRepository
from domain.models import User
from domain.typing import EntityList, Response
from infrastructure.auth import UtilsEntityAuth

if TYPE_CHECKING:
    from uuid import UUID

    from litestar import Request

    from domain.auth import EntityAuth


class UserRepository(IRepository):
    _repository: BaseRepository = BaseRepository(User)
    _auth: EntityAuth = UtilsEntityAuth

    @classmethod
    async def get_all(
            cls,
            request: Request,
            page: int,
            offset: int,
            is_removing: bool,
            params: dict,
    ) -> pagination_generate(UserRead):
        auth = cls._auth(request)
        await auth.verify(auth)
        users = await cls._repository.get_entity(
            page=page,
            offset=offset,
            is_removing=is_removing,
            params=params,
        )
        users.data = [UserRead.from_orm(user) for user in users.data]
        return users

    @classmethod
    async def get_one(cls, entity_id: UUID, request: Request) -> UserRead:
        auth = cls._auth(request)
        await auth.verify(auth)
        user = await cls._repository.query_entity(id=entity_id)
        return UserRead.from_orm(user)

    @classmethod
    async def create(cls, data: UserCreate, request: Request) -> UserRead:
        auth = cls._auth(request)
        await auth.verify(auth)
        user = await cls._repository.create_entity(data.model_dump(exclude_none=True))
        return UserRead.from_orm(user)

    @classmethod
    async def update(cls, entity_id: UUID, data: UserUpdate, request: Request) -> UserRead:
        auth = cls._auth(request)
        await auth.verify(auth)
        user = await cls._repository.update_entity(entity_id, data.model_dump(exclude_unset=True))
        return UserRead.from_orm(user)

    @classmethod
    async def delete(cls, entity_id: UUID, request: Request) -> Response:
        auth = cls._auth(request)
        await auth.verify(auth)
        await cls._repository.delete_entity(entity_id)
        return Response(message="User deleted")


    @classmethod
    async def soft_delete(cls, entity_id: UUID, request: Request, is_removing: bool) -> Response:
        auth = cls._auth(request)
        await auth.verify(auth)
        await cls._repository.soft_delete_entity(entity_id, is_removing)
        if is_removing:
            return Response(message="Message deleted")
        return Response(message="Message restored")


    @classmethod
    async def soft_delete_batch(cls, data: EntityList, request: Request, is_removing: bool) -> Response:
        auth = cls._auth(request)
        await auth.verify(auth)
        [await cls._repository.soft_delete_entity(entity_id, is_removing) for entity_id in data.ids]
        if is_removing:
            return Response(message="Message deleted")
        return Response(message="Message restored")
