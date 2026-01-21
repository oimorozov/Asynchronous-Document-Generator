from fastapi import APIRouter, UploadFile, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse

from src.db.controllers.input_files_controller import save_input_file
from src.rabbitmq.message_broker import publish_msg
from src.minio.minio import client, BUCKET_INPUT_FILE

router = APIRouter()

@router.get("/download/{filename}", response_class=StreamingResponse)
async def get_file_and_send_http_request(filename: str, request: Request):
    """
    Ручка для загрузки файла на клиенте
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