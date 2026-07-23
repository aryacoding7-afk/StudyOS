from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.file import File


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_document(
        self,
        file: File,
        content: str,
        page_count: int,
    ) -> Document:
        document = Document(
            file=file,
            content=content,
            page_count=page_count,
        )

        self.db.add(document)

        return document