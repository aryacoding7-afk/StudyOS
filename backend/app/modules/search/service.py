import logging

from sqlalchemy.orm import Session

from app.core.config import settings
from app.modules.search.repository import SearchRepository
from app.modules.search.schemas import (
    SearchRequest,
    SearchResponse,
    SearchResult,
)
from app.utils.embeddings import generate_embedding

logger = logging.getLogger(__name__)


class SearchService:
    def __init__(self, db: Session):
        self.repository = SearchRepository(db)

    def search(
        self,
        request: SearchRequest,
    ) -> SearchResponse:

        logger.info(
            "Starting semantic search for document %s",
            request.document_id,
        )

        try:
            # Generate embedding for the user's query
            query_embedding = generate_embedding(request.query)

            logger.info(
                "Generated embedding for search query"
            )

            # Retrieve the closest chunks
            chunks = self.repository.search(
                document_id=request.document_id,
                embedding=query_embedding,
                top_k=settings.TOP_K,
            )

            logger.info(
                "Repository returned %d matching chunks",
                len(chunks),
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

            logger.info(
                "Semantic search completed successfully"
            )

            return SearchResponse(results=results)

        except Exception:
            logger.exception(
                "Semantic search failed for document %s",
                request.document_id,
            )
            raise