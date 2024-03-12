from __future__ import annotations

from typing import TYPE_CHECKING

from app.interfaces import IRepository
from app.schemas import MessageCreate, MessageCreateEvent, MessageRead, MessageUpdate, pagination_generate
from domain import BaseRepository
from domain.models import Message, User
from domain.typing import EntityList, Response
from infrastructure.auth import UtilsEntityAuth

if TYPE_CHECKING:
    from uuid import UUID

    from litestar import Request

    from domain.auth import EntityAuth


class MessageRepository(IRepository):
    _message_repository: BaseRepository = BaseRepository(Message)
    _user_repository: BaseRepository = BaseRepository(User)
    _auth: EntityAuth = UtilsEntityAuth

    @classmethod
    async def get_all(
            cls,
            request: Request,
            page: int,
            offset: int,
            is_removing: bool,
            params: dict,
    ) -> pagination_generate(MessageRead):
        auth = cls._auth(request)
        await auth.verify(auth)
        messages = await cls._message_repository.get_entity(
            page=page,
            offset=offset,
            is_removing=is_removing,
            params=params,
        )
        messages.data = [MessageRead.from_orm(message) for message in messages.data]
        return messages

    @classmethod
    async def get_one(cls, entity_id: UUID, request: Request = None) -> MessageRead:
        auth = cls._auth(request)
        await auth.verify(auth)
        message = await cls._message_repository.query_entity(id=entity_id)
        return MessageRead.from_orm(message)

    @classmethod
    async def create(cls, data: MessageCreate, request: Request = None) -> MessageRead:
        auth = cls._auth(request)
        entity_id = auth.get_jwt_subject()
        user = await auth.verify_user(cls._user_repository, id=entity_id)
        data = MessageCreateEvent(**data.dict(), user_id=user.id)
        message = await cls._message_repository.create_entity(data.model_dump(exclude_none=True))
        return MessageRead.from_orm(message)


    @classmethod
    async def update(cls, entity_id: UUID, data: MessageUpdate, request: Request = None) -> MessageRead:
        auth = cls._auth(request)
        await auth.verify(auth)
        message = await cls._message_repository.update_entity(entity_id, data.model_dump(exclude_unset=True))
        return MessageRead.from_orm(message)

    @classmethod
    async def delete(cls, entity_id: UUID, request: Request = None) -> Response:
        auth = cls._auth(request)
        await auth.verify(auth)
        await cls._message_repository.delete_entity(entity_id)
        return Response(message="Message deleted")


    @classmethod
    async def soft_delete(cls, entity_id: UUID, request: Request, is_removing: bool) -> Response:
        auth = cls._auth(request)
        await auth.verify(auth)
        await cls._message_repository.soft_delete_entity(entity_id, is_removing)
        if is_removing:
            return Response(message="Message deleted")
        return Response(message="Message restored")


    @classmethod
    async def soft_delete_batch(cls, data: EntityList, request: Request, is_removing: bool) -> Response:
        auth = cls._auth(request)
        await auth.verify(auth)
        [await cls._message_repository.soft_delete_entity(entity_id, is_removing) for entity_id in data.ids]
        if is_removing:
            return Response(message="Message deleted")
        return Response(message="Message restored")
