import uvicorn
from litestar import Litestar, Router
from litestar.openapi import OpenAPIConfig, OpenAPIController
from litestar.openapi.spec import Components, SecurityScheme

from api import chat_controller, message_controller, system_controller, websocket_controller
from api.middleware import cors_config


class MyOpenAPIController(OpenAPIController):
    path = "/api-message/docs"


controller = Router("/api-message/v1", route_handlers=[
    system_controller, chat_controller, message_controller, websocket_controller,
])

app = Litestar(
    route_handlers=[controller],
    openapi_config=OpenAPIConfig(
        title="Общение Коммуникатор",
        version="1.0.0",
        openapi_controller=MyOpenAPIController,
        security=[{"BearerToken": []}],
        components=Components(
            security_schemes={
                "BearerToken": SecurityScheme(
                    type="http",
                    scheme="bearer",
                ),
            },
        ),
    ),
    cors_config=cors_config,
)


def dev() -> None:
    uvicorn.run("api.message:app", reload=True, port=9002)


if __name__ == "__main__":
    dev()
