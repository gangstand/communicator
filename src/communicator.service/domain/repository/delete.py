from uuid import UUID

from sqlalchemy import select

from domain.logger import logger
from domain.typing import ModelType, Result
from infrastructure.database import async_session


class MixinDelete:
    @staticmethod
    async def delete(model: ModelType, entity_id: UUID) -> Result:
        async with async_session() as session:
            try:
                entity = (await session.execute(select(model).filter_by(id=entity_id))).unique().scalar_one()
                await session.delete(entity)
                await session.commit()
                return Result.ok(entity)
            except Exception as e:
                logger.error(e)
                await session.rollback()
                return Result.fail(e)
            finally:
                await session.close()
