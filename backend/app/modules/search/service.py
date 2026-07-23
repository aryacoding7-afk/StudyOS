from sqlalchemy.orm import Session
from app.core.config import settings 

from app.modules.search.repository import SearchRepository
from app.modules.search.schemas import (
    SearchRequest,
    SearchResponse,
    SearchResult,
)
from app.utils.embeddings import generate_embedding


class SearchService:
    def __init__(self, db: Session):
        self.repository = SearchRepository(db)

    def search(
        self,
        request: SearchRequest,
    ) -> SearchResponse:

        # Generate embedding for the user's query
        query_embedding = generate_embedding(request.query)

        # Retrieve the closest chunks
        chunks = self.repository.search(
            document_id=request.document_id,
            embedding=query_embedding,
            top_k=settings.TOP_K,
        )
        # Convert ORM objects to response models
        results = [
            SearchResult(
                chunk_index=chunk.chunk_index,
                page_number=chunk.page_number,
                content=chunk.content,
                similarity=1 - distance,
            )
            for chunk, distance in chunks
        ]

        return SearchResponse(results=results)