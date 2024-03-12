from litestar import get

from domain.typing import Response


@get(path="/healthcheck", tags=["System"])
async def healthcheck() -> Response:
    return Response(message="OK")
