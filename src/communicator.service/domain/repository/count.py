from sqlalchemy import func, select

from domain.logger import logger
from domain.repository.utils import Utils
from domain.typing import ModelType, Result
from infrastructure.database import async_session


class Count(Utils):
    async def count_row_model(self, model: ModelType, is_removing: bool, params: dict) -> Result:
        async with async_session() as session:
            try:
                query = select(func.count()).select_from(model).filter_by(is_removing=is_removing)

                if params:
                    query = await self.search(params, model, query)

                entity = await session.execute(query)
                return Result.ok(int(entity.unique().scalar()))
            except Exception as e:
                logger.error(e)
                await session.rollback()
                return Result.fail(e)
            finally:
                await session.close()
