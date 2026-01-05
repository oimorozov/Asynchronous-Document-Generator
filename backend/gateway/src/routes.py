from fastapi import APIRouter, UploadFile

from src.db.input_files_controller import save_input_file
from src.message_broker import publish_msg
from src.minio import client, BUCKET_INPUT_FILE

router = APIRouter()

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
    await save_input_file(filename=file.filename)
    await publish_msg(filename=file.filename)
    return {"status": "uploaded", "filename": file.filename}
