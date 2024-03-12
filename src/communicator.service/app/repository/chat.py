from __future__ import annotations

from typing import TYPE_CHECKING

from app.interfaces import IRepository
from app.schemas import ChatCreate, ChatRead, ChatUpdate, pagination_generate
from domain import BaseRepository
from domain.models import Chat
from domain.typing import EntityIdRead, EntityList, Response
from infrastructure import ID_MANAGER
from infrastructure.auth import UtilsEntityAuth

if TYPE_CHECKING:
    from uuid import UUID

    from litestar import Request

    from domain.auth import EntityAuth


class ChatRepository(IRepository):
    _repository: BaseRepository = BaseRepository(Chat)
    _auth: EntityAuth = UtilsEntityAuth

    @classmethod
    async def get_all(
            cls,
            request: Request,
            page: int,
            offset: int,
            is_removing: bool,
            params: dict,
    ) -> pagination_generate(ChatRead):
        auth = cls._auth(request)
        await auth.verify(auth)
        chats = await cls._repository.get_entity(
            page=page,
            offset=offset,
            is_removing=is_removing,
            params=params,
        )
        chats.data = [ChatRead.from_orm(chat) for chat in chats.data]
        return chats

    @classmethod
    async def get_one(cls, entity_id: UUID, request: Request = None) -> ChatRead:
        auth = cls._auth(request)
        await auth.verify(auth)
        chat = await cls._repository.query_entity(id=entity_id)
        return ChatRead.from_orm(chat)

    @classmethod
    async def create(cls, data: ChatCreate, request: Request = None) -> ChatRead:
        auth = cls._auth(request)
        await auth.verify(auth)
        data.users.append(EntityIdRead(id=ID_MANAGER))
        chat = await cls._repository.create_entity(data.model_dump(exclude_none=True))
        return ChatRead.from_orm(chat)

    @classmethod
    async def update(cls, entity_id: UUID, data: ChatUpdate, request: Request = None) -> ChatRead:
        auth = cls._auth(request)
        await auth.verify(auth)
        data.users.append(EntityIdRead(id=ID_MANAGER))
        chat = await cls._repository.update_entity(entity_id, data.model_dump(exclude_unset=True))
        return ChatRead.from_orm(chat)

    @classmethod
    async def delete(cls, entity_id: UUID, request: Request = None) -> Response:
        auth = cls._auth(request)
        await auth.verify(auth)
        await cls._repository.delete_entity(entity_id)
        return Response(message="Chat deleted")

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
