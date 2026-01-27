from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.core.config import settings

from src.models.base import Base

# Движок
engine = create_async_engine(
    url=settings.database_url,
    echo=True
)

# Фабрика сессий
session_factory = async_sessionmaker(engine)

async def get_db():
    async with session_factory() as session:
        yield session

async def create_tables():
    """
    Функция создания таблиц БД
    """
    async with engine.begin() as conn:
        await conn.execute(text("DROP TABLE IF EXISTS input_files CASCADE"))
        await conn.run_sync(Base.metadata.create_all)