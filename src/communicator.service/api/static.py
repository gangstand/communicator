import uvicorn
from litestar import Litestar, Router
from litestar.openapi import OpenAPIConfig, OpenAPIController
from litestar.openapi.spec import Components, SecurityScheme
from litestar.static_files import create_static_files_router

from api.middleware import cors_config
from api.system import static_controller, system_controller


class MyOpenAPIController(OpenAPIController):
    path = "/api-static/docs"


controller = Router("/api-static/v1", route_handlers=[system_controller, static_controller])



app = Litestar(
    route_handlers=[
        create_static_files_router(
            path="/api-static",
            directories=["static"],
            tags=["System"],
        ),
        controller,
    ],
    openapi_config=OpenAPIConfig(
        title="Файлы Коммуникатор",
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
    uvicorn.run("api.static:app", reload=True, port=9001)


if __name__ == "__main__":
    dev()
