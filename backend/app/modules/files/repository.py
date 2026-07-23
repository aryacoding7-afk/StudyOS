from sqlalchemy.orm import Session

from app.models.file import File
from app.models.user import User


class FilesRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_file(
        self,
        filename: str,
        filepath: str,
        owner: User,
    ) -> File:
        file = File(
            filename=filename,
            filepath=filepath,
            owner=owner,
        )

        self.db.add(file)

        return file

    def get_files(
        self,
        owner: User,
    ) -> list[File]:
        return (
            self.db.query(File)
            .filter(File.owner_id == owner.id)
            .order_by(File.created_at.desc())
            .all()
        )

    def get_file(
        self,
        file_id: str,
        owner: User,
    ) -> File | None:
        return (
            self.db.query(File)
            .filter(
                File.id == file_id,
                File.owner_id == owner.id,
            )
            .first()
        )