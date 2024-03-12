from __future__ import annotations

from typing import TYPE_CHECKING

from app.interfaces import IRepository
from app.schemas import PermissionCreate, PermissionRead, PermissionUpdate, pagination_generate
from domain import BaseRepository
from domain.models import Permission
from domain.typing import EntityList, Response
from infrastructure.auth import UtilsEntityAuth

if TYPE_CHECKING:
    from uuid import UUID

    from litestar import Request

    from domain.auth import EntityAuth


class PermissionRepository(IRepository):
    _repository: BaseRepository = BaseRepository(Permission)
    _auth: EntityAuth = UtilsEntityAuth

    @classmethod
    async def delete(cls, entity_id: UUID, request: Request = None) -> Response:
        auth = cls._auth(request)
        await auth.verify(auth)
        await cls._repository.delete_entity(entity_id)
        return Response(message="Permission deleted")

    @classmethod
    async def get_all(
            cls,
            request: Request,
            page: int,
            offset: int,
            is_removing: bool,
            params: dict,
    ) -> pagination_generate(PermissionRead):
        auth = cls._auth(request)
        await auth.verify(auth)
        permissions = await cls._repository.get_entity(
            page=page,
            offset=offset,
            is_removing=is_removing,
            params=params,
        )
        permissions.data = [PermissionRead.from_orm(permission) for permission in permissions.data]
        return permissions

    @classmethod
    async def get_one(cls, entity_id: UUID, request: Request = None) -> PermissionRead:
        auth = cls._auth(request)
        await auth.verify(auth)
        permission = await cls._repository.query_entity(id=entity_id)
        return PermissionRead.from_orm(permission)

    @classmethod
    async def create(cls, data: PermissionCreate, request: Request = None) -> PermissionRead:
        auth = cls._auth(request)
        await auth.verify(auth)
        permission = await cls._repository.create_entity(data.model_dump(exclude_none=True))
        return PermissionRead.from_orm(permission)

    @classmethod
    async def update(cls, entity_id: UUID, data: PermissionUpdate, request: Request = None) -> PermissionRead:
        auth = cls._auth(request)
        await auth.verify(auth)
        permission = await cls._repository.update_entity(entity_id, data.model_dump(exclude_unset=True))
        return PermissionRead.from_orm(permission)

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
