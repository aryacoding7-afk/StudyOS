from sentence_transformers import SentenceTransformer

# Load once when the application starts
model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def generate_embedding(text: str) -> list[float]:
    """
    Generate a 384-dimensional embedding for the given text.
    """
    embedding = model.encode(
        text,
        normalize_embeddings=True,
    )

    return embedding.tolist()