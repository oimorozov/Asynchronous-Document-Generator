from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from sqlalchemy.orm import DeclarativeBase

from src.config import settings

class Base(DeclarativeBase):
    """
    Интерфейс для моделей БД
    """
    pass

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