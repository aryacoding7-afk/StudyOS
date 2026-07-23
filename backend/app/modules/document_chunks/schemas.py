from dataclasses import dataclass


@dataclass
class ChunkData:
    chunk_index: int
    page_number: int
    content: str
    embedding: list[float]