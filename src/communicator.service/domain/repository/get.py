from __future__ import annotations

from math import ceil

from sqlalchemy import select

from domain.logger import logger
from domain.repository.count import Count
from domain.typing import ModelType, Pagination, Result
from infrastructure.database import async_session


class MixinGet(Count):
    async def get(
            self, *, model: ModelType, page: int, offset: int, is_removing: bool | None, params: dict,
    ) -> Result:
        async with async_session() as session:
            try:
                query = select(model).filter_by(is_removing=is_removing)

                if params:
                    query = await self.search(params, model, query)

                row_count = await self.count_row_model(model, is_removing, params)
                count = row_count.value
                next_page, prev_page = await self.generate_pagination(page, offset, count)

                query = query.offset((page - 1) * offset).limit(offset)
                entity = await session.execute(query)
                data = entity.unique().scalars().all()
                result = Pagination(next=next_page, prev=prev_page, data=data, page=ceil(count / offset))
                return Result.ok(result)
            except Exception as e:
                logger.error(e)
                await session.rollback()
                return Result.fail(e)
            finally:
                await session.close()
