import asyncio

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1 import router
from src.core import message_broker
from src.core.minio import create_buckets
from src.core.database import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("INFO: Инициализация БД")
    await create_tables()
    print("INFO: БД инициализирована")

    print("INFO: Инициализация MinIO")
    create_buckets()
    print("INFO: MinIO инициализирована")

    await message_broker.broker.start()

    yield

    await message_broker.broker.stop()

    print("INFO: Завершение работы")

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router.router)

if __name__ == '__main__':
    asyncio.run(app.run())