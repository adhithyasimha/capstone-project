import numpy as np
import faiss
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def normalize(vecs):
    logger.info(f"Normalizing vectors of shape {vecs.shape}")
    vecs = np.array(vecs)
    if vecs.ndim == 1:
        norm = np.linalg.norm(vecs)
        logger.info(f"1D vector normalization: norm={norm}")
        return vecs / norm
    else:
        norms = np.linalg.norm(vecs, axis=1, keepdims=True)
        logger.info(f"2D vectors normalization: min_norm={norms.min()}, max_norm={norms.max()}")
        return vecs / norms

def build_faiss_index(embeddings: list):
    logger.info(f"Building FAISS index from {len(embeddings)} embeddings")
    embeddings = np.array(embeddings)
    logger.info(f"Embeddings array shape: {embeddings.shape}")
    
    embeddings = normalize(embeddings)
    logger.info(f"Normalized embeddings shape: {embeddings.shape}")

    if embeddings.ndim == 1:
        logger.info("Reshaping 1D embeddings to 2D")
        embeddings = embeddings.reshape(1, -1)

    dim = embeddings.shape[1]
    logger.info(f"Creating FAISS IndexFlatIP with dimension {dim}")
    index = faiss.IndexFlatIP(dim)  # Using inner product for cosine similarity
    
    logger.info(f"Adding {embeddings.shape[0]} embeddings to index")
    index.add(embeddings)
    
    logger.info(f"FAISS index built successfully with {index.ntotal} vectors")
    return index, embeddings
