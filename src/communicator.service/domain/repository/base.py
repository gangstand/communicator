from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from litestar.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

from domain.interfaces.irepository import IBaseRepository
from domain.repository.create import MixinCreate
from domain.repository.delete import MixinDelete
from domain.repository.get import MixinGet
from domain.repository.handle import MixinHandle
from domain.repository.query import MixinQuery
from domain.repository.soft_delete import SoftDeleteMixin
from domain.repository.update import MixinUpdate
from domain.typing import ModelType, Pagination, Result

if TYPE_CHECKING:
    from uuid import UUID


class BaseRepository(
    IBaseRepository,
    MixinGet,
    MixinQuery,
    MixinCreate,
    MixinUpdate,
    MixinDelete,
    SoftDeleteMixin,
    MixinHandle,
):
    def __init__(self, model: ModelType) -> None:
        self._model = model

    async def get_entity(
            self, *,
            page: int,
            offset: int,
            is_removing: bool,
            params: dict,
    ) -> Pagination:
        result = await self.get(
            model=self._model,
            page=page,
            offset=offset,
            is_removing=is_removing,
            params=params,
        )
        return await self.handle_result(result)

    async def query_entity(self, **kwargs: dict[str, Any] | str | UUID) -> Result.value:
        result = await self.query(self._model, **kwargs)
        return await self.handle_result(result)

    async def create_entity(self, data: dict) -> Result.value:
        result = await self.create(self._model, data=data)
        match result:
            case Result(_, IntegrityError() as error):
                error = str(error.orig).split("\n")[1]
                message = f"Internal Server Error: IntegrityError. {error}"
                logging.error(message)
                raise HTTPException(
                    detail=message,
                    status_code=422,
                )
        return await self.handle_result(result)

    async def update_entity(self, entity_id: UUID, data: dict) -> Result.value:
        result = await self.update(self._model, entity_id=entity_id, data=data)
        match result:
            case Result(_, IntegrityError() as error):
                error = str(error.orig).split("\n")[1]
                message = f"Internal Server Error: IntegrityError. {error}"
                logging.error(message)
                raise HTTPException(
                    detail=message,
                    status_code=422,
                )
        return await self.handle_result(result)

    async def delete_entity(self, entity_id: UUID) -> Result.value:
        result = await self.delete(self._model, entity_id=entity_id)
        return await self.handle_result(result)

    async def soft_delete_entity(self, entity_id: UUID, is_removing: bool) -> Result.value:
        result = await self.soft_delete(self._model, entity_id=entity_id, is_removing=is_removing)
        return await self.handle_result(result)
