from uuid import UUID

from pydantic import BaseModel


class ChatRequest(BaseModel):
    document_id: UUID
    conversation_id: UUID
    question: str


class ChatSource(BaseModel):
    page_number: int
    similarity: float
    excerpt: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[ChatSource]