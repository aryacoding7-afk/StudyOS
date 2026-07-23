from app.models.user import User
from app.modules.notes.repository import NotesRepository
from app.modules.notes.schemas import NoteCreate
from sqlalchemy.orm import Session


class NotesService:
    def __init__(self, db: Session):
        self.repository = NotesRepository(db)

    def create_note(
        self,
        note: NoteCreate,
        current_user: User,
    ):
        return self.repository.create_note(
            title=note.title,
            content=note.content,
            owner=current_user,
        )