import uvicorn
from litestar import Litestar, Router
from litestar.openapi import OpenAPIConfig, OpenAPIController
from litestar.openapi.spec import Components, SecurityScheme

from api import auth_controller, system_controller
from api.middleware import cors_config


class MyOpenAPIController(OpenAPIController):
    path = "/api-auth/docs"


controller = Router("/api-auth/v1", route_handlers=[system_controller, auth_controller])

app = Litestar(
    route_handlers=[controller],
    openapi_config=OpenAPIConfig(
        title="Авторизация Коммуникатор",
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
    ), cors_config=cors_config,
)


def dev() -> None:
    uvicorn.run("api.auth:app", reload=True, port=8000)


if __name__ == "__main__":
    dev()
