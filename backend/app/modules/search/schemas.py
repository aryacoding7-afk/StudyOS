from pydantic import BaseModel
from pydantic import BaseModel


from uuid import UUID
from pydantic import BaseModel


class SearchRequest(BaseModel):
    document_id: UUID
    query: str

class SearchResult(BaseModel):
    chunk_index: int
    page_number: int
    content: str
    similarity: float


class SearchResponse(BaseModel):
    results: list[SearchResult]