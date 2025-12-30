import asyncio
from fastapi import FastAPI

from src.document_router import router

app = FastAPI()

@app.get("/")
async def root():
    return {"Hello": "World"}

app.include_router(router)

if __name__ == '__main__':
    asyncio.run(app.run())