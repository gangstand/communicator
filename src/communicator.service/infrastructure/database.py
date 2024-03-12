from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta

from domain.logger import logger
from infrastructure.settings import DataBaseSettings

database_settings = DataBaseSettings()

DATABASE_URL = f"postgresql+asyncpg://{database_settings.user}:{database_settings.password}@{database_settings.host}:{database_settings.port}/{database_settings.name}"

Base: DeclarativeMeta = declarative_base()

engine = create_async_engine(DATABASE_URL)

async_session = async_sessionmaker(
    engine, class_=AsyncSession,
)


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with async_session() as session:
            yield session
    except Exception as e:
        logger.error(e)
    finally:
        await session.close()
