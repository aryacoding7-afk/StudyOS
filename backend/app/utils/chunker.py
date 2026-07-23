from typing import List


def chunk_text(
    text: str,
    chunk_size: int = 800,
    overlap: int = 100,
) -> List[str]:
    """
    Split text into overlapping chunks.

    Example:
        chunk_size = 800
        overlap = 100

    Chunk 1:
    0 ---------------------- 800

    Chunk 2:
              700 ---------------------- 1500
    """

    if chunk_size <= overlap:
        raise ValueError(
            "chunk_size must be greater than overlap."
        )

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks