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

    def get_note(
        self,
        note_id: str,
        owner: User,
    ) -> Note | None:
        return (
            self.db.query(Note)
            .filter(
                Note.id == note_id,
                Note.owner_id == owner.id,
            )
            .first()
        )

    def update_note(
        self,
        note: Note,
        title: str,
        content: str,
    ) -> Note:
        note.title = title
        note.content = content

        self.db.commit()
        self.db.refresh(note)

        return note

    def delete_note(
        self,
        note: Note,
    ):
        self.db.delete(note)
        self.db.commit()