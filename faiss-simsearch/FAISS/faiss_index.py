import numpy as np
import faiss

def normalize(vecs):
    vecs = np.array(vecs)
    if vecs.ndim == 1:
        return vecs / np.linalg.norm(vecs)
    return vecs / np.linalg.norm(vecs, axis=1, keepdims=True)

def build_faiss_index(embeddings: list):
    embeddings = np.array(embeddings)
    embeddings = normalize(embeddings)

    if embeddings.ndim == 1:
        embeddings = embeddings.reshape(1, -1)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  # Using inner product for cosine similarity
    index.add(embeddings)
    return index, embeddings
