import os, pickle
import redis
import faiss
import numpy as np
from openai import OpenAI
from config import REDIS_URL, EMBED_DIM

# Redis để lưu từng chunk embedding -> text
r = redis.from_url(REDIS_URL)
# FAISS index
index = faiss.IndexFlatL2(EMBED_DIM)

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def embed_text(text: str) -> np.ndarray:
    resp = client.embeddings.create(
        model='text-embedding-3-small', input=[text]
    )
    return np.array(resp.data[0].embedding, dtype='float32')


def add_document(name: str, content: str):
    # Tách chunk đơn giản
    chunks = [content[i:i+1000] for i in range(0, len(content), 1000)]
    for i, chunk in enumerate(chunks):
        vec = embed_text(chunk)
        index.add(vec.reshape(1, -1))
        # lưu metadata: key=idx -> text
        rid = index.ntotal - 1
        r.hset('docs', rid, chunk)


def query_similar(query: str, topk: int=3):
    qv = embed_text(query).reshape(1, -1)
    D, I = index.search(qv, topk)
    return [r.hget('docs', int(idx)).decode() for idx in I[0]]

