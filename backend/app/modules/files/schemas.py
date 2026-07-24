from uuid import UUID

from pydantic import BaseModel


class FileUploadResponse(BaseModel):
    file_id: UUID
    document_id: UUID
    filename: str
    filepath: str
    page_count: int