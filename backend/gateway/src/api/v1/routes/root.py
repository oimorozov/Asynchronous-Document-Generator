from fastapi import APIRouter

from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/", response_class=JSONResponse)
async def root():
    return {
        "message": "root"
    }