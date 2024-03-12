from __future__ import annotations

from typing import TYPE_CHECKING

from app.interfaces import IRepository
from app.schemas import RoleCreate, RoleRead, RoleUpdate, pagination_generate
from domain import BaseRepository
from domain.models import Role
from domain.typing import EntityList, Response
from infrastructure.auth import UtilsEntityAuth

if TYPE_CHECKING:
    from uuid import UUID

    from litestar import Request

    from domain.auth import EntityAuth


class RoleRepository(IRepository):
    _repository: BaseRepository = BaseRepository(Role)
    _auth: EntityAuth = UtilsEntityAuth

    @classmethod
    async def get_all(
            cls,
            request: Request,
            page: int,
            offset: int,
            is_removing: bool,
            params: dict,
    ) -> pagination_generate(RoleRead):
        auth = cls._auth(request)
        await auth.verify(auth)
        roles = await cls._repository.get_entity(
            page=page,
            offset=offset,
            is_removing=is_removing,
            params=params,
        )
        roles.data = [RoleRead.from_orm(role) for role in roles.data]
        return roles

    @classmethod
    async def get_one(cls, entity_id: UUID, request: Request = None) -> RoleRead:
        auth = cls._auth(request)
        await auth.verify(auth)
        role = await cls._repository.query_entity(id=entity_id)
        return RoleRead.from_orm(role)

    @classmethod
    async def create(cls, create_data: RoleCreate, request: Request = None) -> RoleRead:
        auth = cls._auth(request)
        await auth.verify(auth)
        role = await cls._repository.create_entity(create_data.model_dump(exclude_none=True))
        return RoleRead.from_orm(role)

    @classmethod
    async def update(cls, entity_id: UUID, update_data: RoleUpdate, request: Request = None) -> RoleRead:
        auth = cls._auth(request)
        await auth.verify(auth)
        role = await cls._repository.update_entity(entity_id, update_data.model_dump(exclude_unset=True))
        return RoleRead.from_orm(role)

    @classmethod
    async def delete(cls, entity_id: UUID, request: Request = None) -> Response:
        auth = cls._auth(request)
        await auth.verify(auth)
        await cls._repository.delete_entity(entity_id)
        return Response(message="Role deleted")


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
