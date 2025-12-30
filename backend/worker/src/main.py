import asyncio

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import create_tables
from src.models.input_file import InputFile
from src.models.output_file import OutputFile

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"Hello": "World"}

if __name__ == '__main__':
    asyncio.run(app.run())