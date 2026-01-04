from faststream.rabbit import RabbitBroker

from fastapi import UploadFile, APIRouter
from fastapi.responses import StreamingResponse

from src.config import settings

from src.minio import client, BUCKET_INPUT_FILE, BUCKET_OUTPUT_FILE

broker = RabbitBroker(settings.RABBITMQ_URL)

router = APIRouter()

async def publish_msg(filename: str):
    """
    Публикует сообщение в RabbitMQ
    """
    await broker.publish(
        message=f"{filename}",
        queue="input_files"
    )
    return {
        "data": "Success"
    }

@router.post("/upload")
async def upload_file_and_publish_msg(file: UploadFile):
    """
    Ручка для получения файла с фронта
    """
    client.put_object(
        bucket_name=BUCKET_INPUT_FILE,
        object_name=file.filename,
        data=file.file,
        length=file.size,
        content_type=file.content_type
    )
    await publish_msg(filename=file.filename)
    return {"status": "uploaded", "filename": file.filename}
