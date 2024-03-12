from uuid import UUID

from litestar import Controller, Request, delete, get, patch, post

from app.repository import MessageRepository
from app.schemas import MessageCreate, MessageRead, MessageUpdate, pagination_generate
from domain.typing import EntityList, OptionalUUID, Response


class Message(Controller):
    _message_repository = MessageRepository

    @get()
    async def get_messages(
            self,
            request: Request,
            chat_id: OptionalUUID = None,
            page: int = 1,
            offset: int = 50,
            is_removing: bool = False,
    ) -> pagination_generate(MessageRead):
        params = {"chat_id": chat_id}
        return await self._message_repository.get_all(request, page, offset, is_removing, params)

    @get("/{message_id:uuid}")
    async def get_message(self, message_id: UUID, request: Request) -> MessageRead:
        return await self._message_repository.get_one(message_id, request)

    @patch("/{message_id:uuid}", status_code=201)
    async def update_message(self, message_id: UUID, data: MessageUpdate, request: Request) -> MessageRead:
        return await self._message_repository.update(message_id, data, request)

    @post(status_code=201)
    async def create_message(self, data: MessageCreate, request: Request) -> MessageRead:
        return await self._message_repository.create(data, request)

    @delete("/{message_id:uuid}", status_code=201)
    async def delete_message(self, message_id: UUID, request: Request) -> Response:
        return await self._message_repository.delete(message_id, request)

    @patch("/soft_delete/{message_id:uuid}", status_code=201)
    async def soft_delete_message(self, message_id: UUID, is_removing: bool, request: Request) -> Response:
        return await self._message_repository.soft_delete(message_id, request, is_removing)

    @patch("/soft_delete/batch", status_code=201)
    async def soft_delete_batch_message(self, data: EntityList, is_removing: bool, request: Request) -> Response:
        return await self._message_repository.soft_delete_batch(data, request, is_removing)
