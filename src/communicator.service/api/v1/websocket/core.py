from litestar import WebSocket
from litestar.handlers import WebsocketListener

from domain.events import manager_websocket


class WebSocketController(WebsocketListener):
    _manager = manager_websocket

    async def on_accept(self, socket: WebSocket, token: str) -> None:
        await self._manager.add_connection(socket, token)

    async def on_disconnect(self, socket: WebSocket) -> None:
        await self._manager.remove_connection(socket)

    async def on_receive(self, data: str) -> str:
        return data
