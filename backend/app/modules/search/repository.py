from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk


class SearchRepository:
    def __init__(self, db: Session):
        self.db = db

    def search(
        self,
        document_id,
        embedding: list[float],
        top_k: int = 5,
    ):
        return (
            self.db.query(
                DocumentChunk,
                DocumentChunk.embedding.cosine_distance(
                    embedding
                ).label("distance"),
            )
            .filter(
                DocumentChunk.document_id == document_id
            )
            .order_by(
                DocumentChunk.embedding.cosine_distance(embedding)
            )
            .limit(top_k)
            .all()
        )   