from uuid import UUID

from sqlalchemy import select

from domain.logger import logger
from domain.repository.utils import Utils
from domain.typing import ModelType, Result
from infrastructure.database import async_session


class MixinUpdate(Utils):
    async def update(self, model: ModelType, entity_id: UUID, data: dict) -> Result:
        async with async_session() as session:
            try:
                entity = (await session.execute(select(model).filter_by(id=entity_id))).unique().scalar_one()
                entity = await self.entity_with_relationships(model, entity, data, session)
                await session.commit()
                await session.refresh(entity)
                return Result.ok(entity)
            except Exception as e:
                logger.error(e)
                await session.rollback()
                return Result.fail(e)
            finally:
                await session.close()
