from app.utils.chunker import chunk_text

text = "A" * 2500

chunks = chunk_text(text)

print(f"Chunks: {len(chunks)}")

for i, chunk in enumerate(chunks):
    print(i, len(chunk))