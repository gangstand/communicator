from litestar import Router

from .core import WebSocketController

websocket_controller = Router(path="/ws", route_handlers=[WebSocketController], tags=["WebSocket"])
