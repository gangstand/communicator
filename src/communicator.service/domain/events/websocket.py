from __future__ import annotations

from typing import TYPE_CHECKING

from litestar.exceptions import HTTPException

from app.schemas.chat import ChatRead
from app.schemas.message import MessageRead
from domain.logger import logger
from domain.models.chat import Chat
from domain.models.user import User

if TYPE_CHECKING:
    from litestar import WebSocket
    from sqlalchemy import UUID

    from domain.auth import EntityAuth

from domain.models.message import Message
from domain.repository import BaseRepository
from infrastructure.auth import UtilsEntityAuth


class WebSocketManager:
    _auth: EntityAuth = UtilsEntityAuth
    _user_repository: BaseRepository = BaseRepository(User)
    _massage_repository: BaseRepository = BaseRepository(Message)

    def __init__(self) -> None:
        self.websocket_connections: dict[UUID, WebSocket] = {}

    async def add_connection(self, socket: WebSocket, token: str) -> None:
        try:
            try:
                print(self.websocket_connections)
                user_id = await self.authenticate_user(token)
                self.websocket_connections[user_id] = socket
            except HTTPException as e:
                await self.handle_error(socket, e)
                await socket.close()
        except Exception as e:
            print(e)

    async def authenticate_user(self, token: str) -> UUID:
        auth = self._auth()
        auth.jwt_required(auth_from="websocket", token=token)
        entity_id = auth.get_raw_jwt(token)["sub"]
        user = await auth.verify_user(self._user_repository, id=entity_id)
        return user.id

    @staticmethod
    async def handle_error(socket: WebSocket, e: HTTPException) -> None:
        logger.error(f"WebSocket error: {e}")
        await socket.send_text(str(e))

    async def remove_connection(self, disc_socket: WebSocket) -> None:
        keys_to_remove = []

        for user_id, socket in self.websocket_connections.items():
            if socket == disc_socket:
                keys_to_remove.append(user_id)

        for user_id in keys_to_remove:
            self.websocket_connections.pop(user_id)

    async def send_message_to_user(self, user_id: UUID, message: dict) -> None:
        print(self.websocket_connections)
        for uid, socket in self.websocket_connections.items():
            if uid == user_id:
                await socket.send_text(str(message))

    async def event_message(self, target: Message) -> None:
        repository_chat = BaseRepository(Chat)
        message = MessageRead(**target.__dict__)
        chat_id = message.chat_id
        chat_entity = await repository_chat.query_entity(id=chat_id)
        chat = ChatRead.from_orm(chat_entity)
        [await self.send_message_to_user(user.id, message.model_dump(mode="json")) for user in chat.users]
