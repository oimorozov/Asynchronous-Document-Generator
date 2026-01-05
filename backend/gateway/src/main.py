import asyncio

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import routes, message_broker

from src.minio import create_buckets

from src.db.database import create_tables
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

    await message_broker.broker.start()

    yield

    await message_broker.broker.stop()

    print("INFO: Завершение работы")

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:8001",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {
        "message": "root"
    }

app.include_router(routes.router)

if __name__ == '__main__':
    asyncio.run(app.run())