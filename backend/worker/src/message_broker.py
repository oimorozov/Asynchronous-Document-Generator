from pydantic import BaseModel
from faststream.rabbit import RabbitBroker
from minio.commonconfig import CopySource
from sqlalchemy import update

from src.config import settings
from src.database import session_factory
from src.minio import client, BUCKET_OUTPUT_FILE, BUCKET_INPUT_FILE
from src.models.input_file import InputFile

broker = RabbitBroker(settings.RABBITMQ_URL)

class InputFileMessage(BaseModel):
    id: int
    filename: str
    s3_path: str

@broker.subscriber(queue="input_files")
async def sub_msg(message: InputFileMessage):
    print(f"INFO (worker): received message. Content: {message.filename}")
    async with session_factory() as session:
        await session.execute(
            update(InputFile)
            .where(InputFile.id == message.id)
            .values(status="PROCESSING")
        )
        await session.commit()

    output_name = f"processed_{message.s3_path}"
    try:
        client.copy_object(
            BUCKET_OUTPUT_FILE,
            output_name,
            CopySource(BUCKET_INPUT_FILE, message.s3_path)
        )
        async with session_factory() as session:
            await session.execute(
                update(InputFile)
                .where(InputFile.id == message.id)
                .values(status="COMPLETED", result_s3_path=output_name)
            )
            await session.commit()
    except Exception:
        async with session_factory() as session:
            await session.execute(
                update(InputFile)
                .where(InputFile.id == message.id)
                .values(status="FAILED")
            )
            await session.commit()
        raise
