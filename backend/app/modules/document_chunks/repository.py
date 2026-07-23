from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk

from app.modules.document_chunks.schemas import ChunkData


class DocumentChunkRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_chunks(
        self,
        document: Document,
        chunks: list[ChunkData],
    ) -> list[DocumentChunk]:

        saved_chunks = []

        for chunk_data in chunks:
            chunk = DocumentChunk(
                document=document,
                chunk_index=chunk_data.chunk_index,
                page_number=chunk_data.page_number,
                content=chunk_data.content,
                embedding=chunk_data.embedding,
            )

            self.db.add(chunk)
            saved_chunks.append(chunk)

        return saved_chunks