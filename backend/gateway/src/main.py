import asyncio

from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.document_router import router
from src.database import create_tables
from src.models.input_file import InputFile
from src.models.output_file import OutputFile

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Запускаем создание таблиц...")
    await create_tables()
    print("Таблицы проверены/созданы")
    yield
    print("Сервер останавливается")

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"Hello": "World"}

app.include_router(router)

if __name__ == '__main__':
    asyncio.run(app.run())