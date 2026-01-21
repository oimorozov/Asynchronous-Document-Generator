from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse

from src.services.MinioService import minioService

router = APIRouter()

@router.post("/upload", response_class=JSONResponse)
async def upload_file(file: UploadFile):
    """
    Ручка для получения файла с фронта
    """
    minioService.save_obj(file, minioService.BUCKET_INPUT_FILE)

    await save_input_file(filename=file.filename) # Repository

    await publish_msg(filename=file.filename) # Broker

    return {
        "status": "uploaded",
        "filename": file.filename
    }