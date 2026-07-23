from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.modules.auth.dependencies import get_current_user
from app.modules.notes.schemas import NoteCreate, NoteResponse
from app.modules.notes.service import NotesService

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


@router.post(
    "",
    response_model=NoteResponse,
    status_code=201,
)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NotesService(db)
    return service.create_note(note, current_user)