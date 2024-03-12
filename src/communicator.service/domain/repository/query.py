from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy import and_, select

from domain.logger import logger
from domain.typing import ModelType, Result
from infrastructure.database import async_session

if TYPE_CHECKING:
    from uuid import UUID


class MixinQuery:
    @staticmethod
    async def query(model: ModelType, **kwargs: dict[str, Any] | str | UUID) -> Result:
        async with async_session() as session:
            try:
                query = select(model).filter(and_(*[getattr(model, key) == value for key, value in kwargs.items()]))
                entity = await session.execute(query)
                return Result.ok(entity.unique().scalar_one())
            except Exception as e:
                logger.error(e)
                await session.rollback()
                return Result.fail(e)
            finally:
                await session.close()
