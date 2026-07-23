from app.utils.embeddings import generate_embedding

embedding = generate_embedding(
    "Artificial Intelligence is amazing."
)

print(len(embedding))
print(embedding[:10])