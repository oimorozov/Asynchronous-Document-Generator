from urllib.parse import urlparse, urlunparse

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.core.minio import minio_client
from src.core.config import settings
from src.repositories.input_file_repo import InputFileRepository
from datetime import timedelta

router = APIRouter()

@router.get("/status/{task_id}")
async def get_status(task_id: int, db: AsyncSession = Depends(get_db)):
    repo = InputFileRepository(db)
    record = await repo.get_by_id(task_id)
    
    if not record:
        raise HTTPException(status_code=404, detail="Task not found")

    response = {
        "id": record.id,
        "status": record.status,
        "filename": record.filename
    }

    if record.status == "COMPLETED" and record.result_s3_path:
        url = minio_client.presigned_get_object(
            settings.OUTPUT_BUCKET,
            record.result_s3_path,
            expires=timedelta(hours=1)
        )
        if settings.MINIO_PUBLIC_ENDPOINT:
            public_endpoint = settings.MINIO_PUBLIC_ENDPOINT
            if "://" not in public_endpoint:
                public_endpoint = f"http://{public_endpoint}"
            public_parsed = urlparse(public_endpoint)
            parsed = urlparse(url)
            url = urlunparse(
                parsed._replace(
                    scheme=public_parsed.scheme or parsed.scheme,
                    netloc=public_parsed.netloc or parsed.netloc
                )
            )
        response["download_url"] = url

    return response