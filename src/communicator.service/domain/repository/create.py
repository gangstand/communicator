from domain.logger import logger
from domain.repository.utils import Utils
from domain.typing import ModelType, Result
from infrastructure.database import async_session


class MixinCreate(Utils):
    async def create(self, model: ModelType, data: dict) -> Result:
        async with async_session() as session:
            try:
                entity = model()
                entity = await self.entity_with_relationships(model, entity, data, session)
                session.add(entity)
                await session.commit()
                await session.refresh(entity)
                return Result.ok(entity)
            except Exception as e:
                logger.error(e)
                await session.rollback()
                return Result.fail(e)
            finally:
                await session.close()
