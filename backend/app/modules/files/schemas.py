from uuid import UUID
from pydantic import BaseModel, ConfigDict

class FileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    filename: str
    filepath: str