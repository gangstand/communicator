from litestar import Router

from .auth import Auth
from .chat import Chat
from .message import Message
from .permission import Permission
from .role import Role
from .user import User

auth_controller = Router(path="/auth", route_handlers=[Auth], tags=["Authentication"])
permission_controller = Router(path="/permission", route_handlers=[Permission], tags=["Permission"])
role_controller = Router(path="/role", route_handlers=[Role], tags=["Role"])
user_controller = Router(path="/user", route_handlers=[User], tags=["User"])
chat_controller = Router(path="/chat", route_handlers=[Chat], tags=["Chat"])
message_controller = Router(path="/message", route_handlers=[Message], tags=["Message"])
