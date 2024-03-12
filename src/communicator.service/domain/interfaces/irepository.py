from abc import ABC, abstractmethod
from uuid import UUID

from domain.typing import ModelType, Result


class IBaseRepository(ABC):
    @abstractmethod
    def __init__(self, model: ModelType) -> None:
        self._model = model

    @abstractmethod
    async def get_entity(self, page: int, offset: int, is_removing: bool, params: dict) -> Result.value:
        msg = "Implement this method"
        raise NotImplementedError(msg)

    @abstractmethod
    async def query_entity(self, entity_id: UUID) -> Result.value:
        msg = "Implement this method"
        raise NotImplementedError(msg)

    @abstractmethod
    async def create_entity(self, data: dict) -> Result.value:
        msg = "Implement this method"
        raise NotImplementedError(msg)

    @abstractmethod
    async def update_entity(self, entity_id: UUID, data: dict) -> Result.value:
        msg = "Implement this method"
        raise NotImplementedError(msg)

    @abstractmethod
    async def delete_entity(self, entity_id: UUID) -> Result.value:
        msg = "Implement this method"
        raise NotImplementedError(msg)

    @abstractmethod
    async def soft_delete_entity(self, entity_id: UUID, is_removing: bool) -> Result.value:
        msg = "Implement this method"
        raise NotImplementedError(msg)
