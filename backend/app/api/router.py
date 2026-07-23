from fastapi import APIRouter

from app.modules.auth.router import router as auth_router
from app.modules.notes.router import router as notes_router
from app.modules.files.router import router as files_router
from app.modules.search.router import router as search_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(notes_router)
api_router.include_router(files_router)
api_router.include_router(search_router)