from pydantic import BaseModel

from domain.typing import ModelType, OptionalInteger


def pagination_generate(schema: ModelType) -> "PaginationResponse":
    class PaginationResponse(BaseModel):
        data: list[schema]
        next: OptionalInteger
        prev: OptionalInteger
        pages: int

    return type(f"{schema.__name__}PaginationResponse", (PaginationResponse,), {})
