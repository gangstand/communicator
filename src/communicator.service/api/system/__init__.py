from litestar import Router

from .file import File
from .healthcheck import healthcheck

system_controller = Router(path="/system", route_handlers=[healthcheck], tags=["System"])
static_controller = Router(path="/file", route_handlers=[File], tags=["File"])
