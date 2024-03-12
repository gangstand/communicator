from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from domain.typing import ModelType, Query


class Utils:
    @staticmethod
    async def entity_with_relationships(
            model: ModelType, entity: ModelType, data: dict, session: AsyncSession,
    ) -> ModelType:

        unique_ids = set()
        for key, value in data.items():
            if isinstance(value, list):
                unique_entries = []
                for entry in value:
                    if entry["id"] not in unique_ids:
                        unique_entries.append(entry)
                        unique_ids.add(entry["id"])
                data[key] = unique_entries

        for key, value in data.items():
            if not isinstance(value, list):
                setattr(entity, key, value)
            else:
                related_entities = []
                for relation_data in value:
                    entity_id = relation_data.get("id")
                    _model = getattr(model, key).property.mapper.class_
                    related_entity_query = select(_model).filter_by(id=entity_id)
                    related_entity_result = await session.execute(related_entity_query)
                    related_entity = related_entity_result.unique().scalar_one_or_none()
                    if related_entity:
                        related_entities.append(related_entity)
                setattr(entity, key, related_entities)
        return entity

    @staticmethod
    async def generate_pagination(
            page: int,
            offset: int,
            row_count: int,
    ) -> tuple[str | None, str | None]:
        page = max(page, 1)
        next_page = page + 1 if row_count > page * offset else None
        prev_page = page - 1 if page > 1 else None
        return next_page, prev_page

    @staticmethod
    async def search(params: dict, model: ModelType, query: Query) -> Query:
        return query.filter(*(getattr(model, key) == value for key, value in params.items() if value))
