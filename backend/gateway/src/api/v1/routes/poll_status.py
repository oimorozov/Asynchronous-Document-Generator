from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/status/{filename}", response_class=JSONResponse)
async def poll_status(filename: str):
    """
    Ручка для поллинга статуса файла
    """
    return {
        "status": "uploaded",
        "filename": filename
    }