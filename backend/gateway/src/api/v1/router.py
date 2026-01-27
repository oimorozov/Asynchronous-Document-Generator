from fastapi import APIRouter

from src.api.v1.routes import root, upload_file, poll_status

router = APIRouter(prefix="/api/v1")

router.include_router(root.router)
router.include_router(upload_file.router)
router.include_router(poll_status.router)
