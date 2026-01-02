import asyncio

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import create_tables
from src.models.input_file import InputFile
from src.models.output_file import OutputFile

from src import message_broker

@asynccontextmanager
async def lifespan(app: FastAPI):
    await message_broker.broker.start()
    yield
    await message_broker.broker.stop()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"Hello": "World"}

app.include_router(message_broker.router)

if __name__ == '__main__':
    asyncio.run(app.run())