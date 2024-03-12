from uuid import UUID

from litestar import Controller, Request, delete, get, patch, post

from app.repository import ChatRepository
from app.schemas import ChatCreate, ChatRead, ChatUpdate, pagination_generate
from domain.typing import EntityList, Response


class Chat(Controller):
    _chat_repository = ChatRepository

    @get()
    async def get_chats(
            self, request: Request,
            page: int = 1,
            offset: int = 50,
            is_removing: bool = False,
    ) -> pagination_generate(ChatRead):
        params = {}
        return await self._chat_repository.get_all(request, page, offset, is_removing, params)

    @get("/{chat_id:uuid}")
    async def get_chat(self, chat_id: UUID, request: Request) -> ChatRead:
        return await self._chat_repository.get_one(chat_id, request)

    @patch("/{chat_id:uuid}", status_code=201)
    async def update_chat(self, chat_id: UUID, data: ChatUpdate, request: Request) -> ChatRead:
        return await self._chat_repository.update(chat_id, data, request)

    @post(status_code=201)
    async def create_chat(self, data: ChatCreate, request: Request) -> ChatRead:
        return await self._chat_repository.create(data, request)

    @delete("/{chat_id:uuid}", status_code=201)
    async def delete_chat(self, chat_id: UUID, request: Request) -> Response:
        return await self._chat_repository.delete(chat_id, request)

    @patch("/soft_delete/{chat_id:uuid}", status_code=201)
    async def soft_delete_chat(self, chat_id: UUID, is_removing: bool, request: Request) -> Response:
        return await self._chat_repository.soft_delete(chat_id, request, is_removing)

    @patch("/soft_delete/batch", status_code=201)
    async def soft_delete_batch_chat(self, data: EntityList, is_removing: bool, request: Request) -> Response:
        return await self._chat_repository.soft_delete_batch(data, request, is_removing)
