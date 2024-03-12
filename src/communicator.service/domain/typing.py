from dataclasses import dataclass
from datetime import datetime
from typing import Any, Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict

ModelType = TypeVar("ModelType")
V = TypeVar("V")
E = TypeVar("E", bound=Exception)
Result = TypeVar("Result")
OptionalString = str | None
OptionalBoolean = bool | None
OptionalInteger = int | None
OptionalUUID = UUID | None
Query = TypeVar("Query")


class Pagination(BaseModel):
    data: list
    next: OptionalInteger
    prev: OptionalInteger
    page: int


class EntityIdRead(BaseModel):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class EntityList(BaseModel):
    ids: list[UUID]


class EntityRead(EntityIdRead):
    created_at: datetime
    updated_at: datetime
    is_removing: bool

    model_config = ConfigDict(from_attributes=True)


OptionalListEntityIdRead = list[EntityIdRead] | None


@dataclass
class Response:
    message: str


@dataclass(frozen=True, slots=True, match_args=True)
class Result(Generic[V, E]):
    value: V | None
    error: E | None

    def __post_init__(self) -> None:
        if self.value is None and self.error is None:
            msg = "Value or error is required"
            raise ValueError(msg)

        if self.value is not None and self.error is not None:
            msg = "Init value or error only"
            raise ValueError(msg)

    @classmethod
    def ok(cls, value: V) -> "Result[V, Any]":
        return cls(value=value, error=None)

    @classmethod
    def fail(cls, error: E) -> "Result[V, Any]":
        return cls(value=None, error=error)
