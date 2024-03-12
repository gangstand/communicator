from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from domain.logger import logger
from domain.typing import ModelType, Result
from infrastructure.database import async_session


class SoftDeleteMixin:
    async def soft_delete(
            self,
            model: ModelType,
            entity_id: UUID,
            is_removing: bool | None,
    ) -> Result:
        async with async_session() as session:
            try:
                entity = (await session.execute(select(model).filter_by(id=entity_id))).unique().scalar_one()
                await session.execute(
                    update(model)
                    .where(model.id == entity_id)
                    .values(is_removing=is_removing),
                )
                await self._recursive_hide(
                    session=session, model=model,
                    entity_id=entity_id, is_removing=is_removing,
                    parent="parent_id",
                )
                await session.commit()
                await session.refresh(entity)
                return Result.ok(entity)
            except Exception as e:
                logger.error(e)
                await session.rollback()
                return Result.fail(e)
            finally:
                await session.close()

    async def _recursive_hide(
            self,
            *,
            session: AsyncSession,
            model: ModelType,
            entity_id: UUID,
            is_removing: bool | None,
            parent: str,
    ) -> None:
        if getattr(model, parent, False):
            result = await session.execute(select(model).filter(getattr(model, parent) == entity_id))
            entities = result.scalars().all()

            for entity in entities:
                await session.execute(
                    update(model)
                    .where(model.id == entity.id)
                    .values(is_removing=is_removing),
                )
                await self._recursive_hide(
                       session=session, model=model,
                       entity_id=entity_id, is_removing=is_removing,
                       parent=parent,
                )


