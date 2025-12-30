import asyncio

from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.document_router import router
from src.models.input_file import InputFile
from src.models.output_file import OutputFile
from src.database import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 [Startup] Запускаем создание таблиц...")
    await create_tables()
    print("✅ [Startup] Таблицы проверены/созданы!")
    yield
    print("🛑 [Shutdown] Сервер останавливается")

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"Hello": "World"}

app.include_router(router)

if __name__ == '__main__':
    asyncio.run(app.run())