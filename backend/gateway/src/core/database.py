from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.core.config import settings

from src.models.base import Base

# Движок
engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True
)

# Фабрика сессий
session_factory = async_sessionmaker(engine)

async def create_tables():
    """
    Функция создания таблиц БД
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)