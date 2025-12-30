from sqlalchemy import create_engine

from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.config import settings

class Base(DeclarativeBase):
    """
    Интерфейс для моделей БД
    """
    pass

# Движок
engine = create_engine(
    url=settings.DATABASE_URL,
    echo=True
)

# Фабрика сессий
session_factory = sessionmaker(engine)

def create_tables():
    """
    Функция создания таблиц БД
    """
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)