from fastapi import APIRouter, UploadFile, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse

from src.db.controllers.input_files_controller import save_input_file
from src.rabbitmq.message_broker import publish_msg
from src.minio.minio import client, BUCKET_INPUT_FILE

router = APIRouter()

@router.post("/upload", response_class=JSONResponse)
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
    return {
        "status": "uploaded",
        "filename": file.filename
    }

@router.get("/status/{filename}", response_class=JSONResponse)
async def get_file_status(filename: str):
    """
    Ручка для поллинга статуса файла
    """
    return {
        "status": "uploaded",
        "filename": filename
    }

@router.get("/download/{filename}", response_class=StreamingResponse)
async def get_file_and_send_http_request(filename: str, request: Request):
    """
    Ручка ждя загрузки файла на клиенте
    """
    http_client = request.app.state.http_client

    req = http_client.build_request("GET", f"/download/{filename}")
    r = await http_client.send(req, stream=True)

    if r.status_code != 200:
        await r.aclose()
        raise HTTPException(status_code=r.status_code, detail="File not found on worker service")
    
    return StreamingResponse(
        r.aiter_bytes(),
        media_type=r.headers.get("content-type"),
        headers={"Content-Disposition": r.headers.get("content-disposition")}
    )