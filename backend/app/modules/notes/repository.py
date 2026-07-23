from sqlalchemy.orm import Session

from app.models.note import Note
from app.models.user import User


class NotesRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_note(
        self,
        title: str,
        content: str,
        owner: User,
    ) -> Note:
        note = Note(
            title=title,
            content=content,
            owner=owner,
        )

        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)

        return note

    def get_notes(
        self,
        owner: User,
    ) -> list[Note]:
        return (
            self.db.query(Note)
            .filter(Note.owner_id == owner.id)
            .order_by(Note.created_at.desc())
            .all()
        )