import asyncio

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import message_broker

from src.minio import create_buckets

from src.database import create_tables
from src.models.input_file import InputFile
from src.models.output_file import OutputFile

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("INFO: Инициализация БД")
    await create_tables()
    print("INFO: БД инициализирована")

    print("INFO: Инициализация MinIO")
    create_buckets()
    print("INFO: MinIO инициализирована")

    yield
    
    print("INFO: Завершение работы")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"Hello": "World"}

app.include_router(message_broker.router)

if __name__ == '__main__':
    asyncio.run(app.run())