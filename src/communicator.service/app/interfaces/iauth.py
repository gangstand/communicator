from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uuid import UUID

    from domain import TCreate, TEntity, TUpdate


class IAuth(ABC):

    @classmethod
    @abstractmethod
    async def get_one(cls, entity_id: UUID) -> TEntity:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def create(cls, data: TCreate) -> TEntity:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def update(cls, entity_id: UUID, data: TUpdate) -> TEntity:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def login_phone(cls, data: TUpdate) -> TEntity:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def login_email(cls, data: TUpdate) -> TEntity:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def refresh(cls, data: TEntity) -> TEntity:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def update_password(cls, data: TEntity) -> TEntity:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def recovery(cls, data: TEntity) -> TEntity:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def manager_token(cls, data: TEntity) -> TEntity:
        raise NotImplementedError


