from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain import TCreate, TEntity


class IFile(ABC):

    @classmethod
    @abstractmethod
    async def create(cls, data: TCreate) -> TEntity:
        raise NotImplementedError
