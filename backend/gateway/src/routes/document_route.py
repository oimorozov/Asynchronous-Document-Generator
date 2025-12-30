from fastapi import APIRouter, UploadFile

router = APIRouter()

@router.post("/upload_document")
async def post_document(file: UploadFile):
    return file.filename
