import logging
from pathlib import Path
import shutil

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.exceptions import FileTypeNotSupportedException
from app.models.user import User

from app.modules.files.repository import FilesRepository
from app.modules.documents.repository import DocumentRepository
from app.modules.document_chunks.repository import (
    DocumentChunkRepository,
)
from app.modules.document_chunks.schemas import ChunkData
from app.modules.files.schemas import FileUploadResponse

from app.utils.pdf import extract_text
from app.utils.chunker import chunk_text
from app.utils.embeddings import generate_embedding

logger = logging.getLogger(__name__)

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
    ) -> FileUploadResponse:

        # Only allow PDF uploads
        if not file.filename.lower().endswith(".pdf"):
            logger.warning(
                "Rejected upload '%s': unsupported file type",
                file.filename,
            )
            raise FileTypeNotSupportedException()

        # Create user's upload directory
        user_dir = UPLOAD_DIR / str(current_user.id)
        user_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Save uploaded file
        filepath = user_dir / file.filename

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        logger.info(
            "Saved uploaded file '%s' for user %s",
            file.filename,
            current_user.id,
        )

        # Extract text page-by-page
        pages, page_count = extract_text(filepath)

        logger.info(
            "Extracted %d pages from '%s'",
            page_count,
            file.filename,
        )

        # Combine all pages into one document
        full_text = "\n\n".join(
            page.text
            for page in pages
        )

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

            logger.info(
                "Created document %s",
                saved_document.id,
            )

            # Create chunks
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

            logger.info(
                "Created %d chunks",
                len(chunk_objects),
            )

            # Save chunks
            self.chunk_repository.create_chunks(
                document=saved_document,
                chunks=chunk_objects,
            )

            logger.info("Saving upload transaction")

            self.db.commit()

            self.db.refresh(saved_file)
            self.db.refresh(saved_document)

            logger.info(
                "Upload completed successfully for document %s",
                saved_document.id,
            )

            return FileUploadResponse(
                file_id=saved_file.id,
                document_id=saved_document.id,
                filename=saved_file.filename,
                filepath=saved_file.filepath,
                page_count=saved_document.page_count,
            )

        except Exception:
            self.db.rollback()

            if filepath.exists():
                filepath.unlink()

            logger.exception(
                "Failed to upload '%s'",
                file.filename,
            )

            raise