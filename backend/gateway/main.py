from fastapi import FastAPI

app = FastAPI()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        "main:app",
        port=8001,
        reload=True
    )    