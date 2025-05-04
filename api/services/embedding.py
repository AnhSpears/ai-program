import openai
from config import OPENAI_API_KEY
from models.vector_store import add_embeddings, retrieve_context

openai.api_key = OPENAI_API_KEY

def get_embedding(text: str) -> list[float]:
    resp = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )
    return resp["data"][0]["embedding"]

def embed_and_store(text: str, chunk_size: int = 500, overlap: int = 100):
    """
    1. Chia text thành các chunk (~chunk_size tokens), overlap để bảo đảm ngữ cảnh.
    2. Tạo embedding cho từng chunk.
    3. Gọi vector_store.add_embeddings để lưu.
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        chunk = " ".join(words[start:start + chunk_size])
        chunks.append(chunk)
        start += chunk_size - overlap

    embeddings = [get_embedding(c) for c in chunks]
    add_embeddings(chunks, embeddings)

def retrieve_with_context(query: str, top_k: int = 5) -> str:
    """
    1. Tạo embedding từ query.
    2. Lấy top_k chunks, gom lại thành một context string.
    """
    emb = get_embedding(query)
    chunks = retrieve_context(emb, top_k=top_k)
    return "\n---\n".join(chunks)
