from faststream.rabbit import RabbitBroker

from fastapi import APIRouter, UploadFile
from fastapi.responses import StreamingResponse

from src.config import settings

from src.minio import client, BUCKET_OUTPUT_FILE, BUCKET_INPUT_FILE

broker = RabbitBroker(settings.RABBITMQ_URL)

router = APIRouter()

@broker.subscriber(queue="input_files")
async def sub_msg(filename: str):
    print(f"INFO (worker): received message. Content: {filename}")

@router.get("/download/{filename}")
async def get_file_and_publish_msg(filename: str):
    response = client.get_object(BUCKET_INPUT_FILE, filename)
    return StreamingResponse(
        response,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )