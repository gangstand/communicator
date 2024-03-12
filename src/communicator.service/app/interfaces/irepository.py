from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uuid import UUID

    from litestar import Request

    from domain import Response, TCreate, TEntity, TUpdate


class IRepository(ABC):
    @classmethod
    @abstractmethod
    async def get_all(cls, request: Request, page: int, offset: int, is_removing: bool, params: dict) -> list[TEntity]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_one(cls, entity_id: UUID, request: Request) -> TEntity:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def create(cls, data: TCreate, request: Request) -> TEntity:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def update(cls, entity_id: UUID, data: TUpdate, request: Request) -> TEntity:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def delete(cls, entity_id: UUID, request: Request) -> Response:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def soft_delete(cls, entity_id: UUID, request: Request, is_removing: bool) -> Response:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def soft_delete_batch(cls, entity_id: UUID, request: Request, is_removing: bool) -> Response:
        raise NotImplementedError
