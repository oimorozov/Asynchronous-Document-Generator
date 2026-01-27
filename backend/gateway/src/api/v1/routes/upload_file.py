import io
from uuid import uuid4

from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.minio import minio_client, BUCKET_INPUT_FILE
from src.core.message_broker import broker
from src.repositories.input_file_repo import InputFileRepository

router = APIRouter()

@router.post("/upload", response_class=JSONResponse)
async def upload_file(file: UploadFile, db: AsyncSession = Depends(get_db)):
    """
    Ручка для получения файла с фронта
    """
    contents = await file.read()
    object_name = f"{uuid4().hex}_{file.filename}"
    minio_client.put_object(
        bucket_name=BUCKET_INPUT_FILE,
        object_name=object_name,
        data=io.BytesIO(contents),
        length=len(contents),
        content_type=file.content_type or "application/octet-stream"
    )

    repo = InputFileRepository(db)
    record = await repo.create(filename=file.filename, s3_path=object_name)

    await broker.publish(
        {"id": record.id, "filename": record.filename, "s3_path": object_name},
        queue="input_files"
    )

    return {
        "id": record.id,
        "status": record.status,
        "filename": record.filename
    }
