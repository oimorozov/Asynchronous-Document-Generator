from faststream.rabbit.fastapi import RabbitRouter

from fastapi import UploadFile

from src.config import settings

from src.minio import client, BUCKET_INPUT_FILE

router = RabbitRouter(settings.RABBITMQ_URL)

async def publish_msg(filename: str):
    """
    Публикует сообщение в RabbitMQ
    """
    await router.broker.publish(
        message=f"{filename}",
        queue="files"
    )
    return {
        "data": "Success"
    }

@router.post("/upload")
async def upload_file_and_publish_msg(file: UploadFile):
    """
    Ручка для отправки файла
    """
    client.put_object(
        bucket_name=BUCKET_INPUT_FILE,
        object_name=file.filename,
        data=file.file,
        length=file.size,
        content_type=file.content_type
    )
    await publish_msg(filename=file.filename)