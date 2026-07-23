from sqlalchemy.orm import Session

from app.models.user import User
from app.modules.notes.repository import NotesRepository
from app.modules.notes.schemas import NoteCreate
from fastapi import HTTPException, status


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

    def get_notes(
        self,
        current_user: User,
    ):
        return self.repository.get_notes(current_user)

    def get_note(
        self,
        note_id: str,
        current_user: User,
    ):
        note = self.repository.get_note(
            note_id,
            current_user,
        )

        if note is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found",
            )

        return note

    def update_note(
        self,
        note_id: str,
        note_data: NoteCreate,
        current_user: User,
    ):
        note = self.repository.get_note(
            note_id,
            current_user,
        )

        if note is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found",
            )

        return self.repository.update_note(
            note=note,
            title=note_data.title,
            content=note_data.content,
        )

    def delete_note(
        self,
        note_id: str,
        current_user: User,
    ):
        note = self.repository.get_note(
            note_id,
            current_user,
        )

        if note is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found",
            )

        self.repository.delete_note(note)