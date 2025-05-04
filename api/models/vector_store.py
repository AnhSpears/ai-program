import os, pickle
import faiss
import numpy as np

INDEX_FILE = 'faiss.index'
META_FILE  = 'faiss_meta.pkl'

def _load_index(dim: int):
    if os.path.exists(INDEX_FILE) and os.path.exists(META_FILE):
        index = faiss.read_index(INDEX_FILE)
        with open(META_FILE, 'rb') as f: meta = pickle.load(f)
    else:
        index = faiss.IndexFlatL2(dim)
        meta = []
    return index, meta

def _save_index(index, meta):
    faiss.write_index(index, INDEX_FILE)
    with open(META_FILE, 'wb') as f: pickle.dump(meta, f)

def add_embeddings(chunks: list[str], embeddings: list[list[float]]):
    """
    Thêm batch chunks + embedding vào index, lưu metadata (text chunk) để retrieve.
    """
    dim = len(embeddings[0])
    index, meta = _load_index(dim)

    index.add(np.array(embeddings, dtype='float32'))
    meta.extend(chunks)

    _save_index(index, meta)

def retrieve_context(query_embedding: list[float], top_k: int = 5) -> list[str]:
    """
    Search top_k chunk theo cosine (L2 trên embedding đã chuẩn).
    Trả về list đoạn text.
    """
    dim = len(query_embedding)
    index, meta = _load_index(dim)

    D, I = index.search(np.array([query_embedding], dtype='float32'), top_k)
    results = []
    for idx in I[0]:
        if 0 <= idx < len(meta):
            results.append(meta[idx])
    return results
