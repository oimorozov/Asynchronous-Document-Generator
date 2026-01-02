from faststream.rabbit import RabbitBroker

from fastapi import APIRouter, UploadFile
from fastapi.responses import StreamingResponse

from src.config import settings

from src.minio import client, BUCKET_OUTPUT_FILE, BUCKET_INPUT_FILE

broker = RabbitBroker(settings.RABBITMQ_URL)

router = APIRouter()

async def publish_msg(filename: str):
    """
    Публикует сообщение в RabbitMQ
    """
    await broker.publish(
        message=f"{filename}",
        queue="output_files"
    )
    return {
        "data": "Success"
    }

@broker.subscriber(queue="input_files")
async def sub_msg(filename: str):
    print(f"INFO (worker): received message. Content: {filename}")

@router.post("/upload")
async def upload_file_and_publish_msg(file: UploadFile):
    """
    Ручка для отправки файла
    """
    client.put_object(
        bucket_name=BUCKET_OUTPUT_FILE,
        object_name=file.filename,
        data=file.file,
        length=file.size,
        content_type=file.content_type
    )
    await publish_msg(filename=file.filename)
    return {"status": "uploaded", "filename": file.filename}

@router.get("/download/{filename}")
async def get_file_and_publish_msg(filename: str):
    response = client.get_object(BUCKET_INPUT_FILE, filename)
    return StreamingResponse(
        response,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )