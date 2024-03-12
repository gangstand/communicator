import asyncio

from sqlalchemy import event

from domain.events.websocket import WebSocketManager
from domain.models.message import Message

manager_websocket = WebSocketManager()


async def handle_event(target):
    await manager_websocket.event_message(target)


@event.listens_for(Message, "after_insert")
def after_insert_listener(_: None, __: None, target: Message) -> None:
    asyncio.create_task(handle_event(target))
