import asyncio

from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.database import create_tables
from src.minio import create_buckets
from src import message_broker

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    create_buckets()
    await message_broker.broker.start()
    yield
    await message_broker.broker.stop()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"Hello": "World"}

if __name__ == '__main__':
    asyncio.run(app.run())
