from pathlib import Path
import shutil

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models.user import User

from app.modules.files.repository import FilesRepository
from app.modules.documents.repository import DocumentRepository
from app.modules.document_chunks.repository import DocumentChunkRepository
from app.modules.document_chunks.schemas import ChunkData

from app.utils.pdf import extract_text
from app.utils.chunker import chunk_text
from app.utils.embeddings import generate_embedding

UPLOAD_DIR = Path("uploads")


class FilesService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = FilesRepository(db)
        self.document_repository = DocumentRepository(db)
        self.chunk_repository = DocumentChunkRepository(db)

    def upload_file(
        self,
        file: UploadFile,
        current_user: User,
    ):
        # Only allow PDF uploads
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed.",
            )

        # Create user's upload directory
        user_dir = UPLOAD_DIR / str(current_user.id)
        user_dir.mkdir(parents=True, exist_ok=True)

        # Save uploaded file
        filepath = user_dir / file.filename

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text page-by-page
        pages, page_count = extract_text(filepath)

        print("=" * 80)
        print("Extracted PDF Text")
        print("=" * 80)

        for page in pages:
            print(f"Page {page.page_number}")
            print(page.text[:300])
            print("-" * 40)

        # Combine all pages into one document
        full_text = "\n\n".join(page.text for page in pages)

        try:
            # Create file
            saved_file = self.repository.create_file(
                filename=file.filename,
                filepath=str(filepath),
                owner=current_user,
            )

            self.db.flush()

            # Create document
            saved_document = self.document_repository.create_document(
                file=saved_file,
                content=full_text,
                page_count=page_count,
            )

            self.db.flush()

            # Create chunks with page numbers
            chunk_objects = []
            chunk_index = 0

            for page in pages:
                chunks = chunk_text(page.text)

                for chunk in chunks:
                    chunk_objects.append(
                        ChunkData(
                            chunk_index=chunk_index,
                            page_number=page.page_number,
                            content=chunk,
                            embedding=generate_embedding(chunk),
                        )
                    )

                    chunk_index += 1

            # Save chunks
            self.chunk_repository.create_chunks(
                document=saved_document,
                chunks=chunk_objects,
            )

            self.db.commit()

            self.db.refresh(saved_file)

            return saved_file

        except Exception:
            self.db.rollback()

            if filepath.exists():
                filepath.unlink()

            raise