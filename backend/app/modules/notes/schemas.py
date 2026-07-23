from uuid import UUID

from pydantic import BaseModel


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteUpdate(BaseModel):
    title: str
    content: str


class NoteResponse(BaseModel):
    id: UUID
    title: str
    content: str

    model_config = {
        "from_attributes": True,
    }