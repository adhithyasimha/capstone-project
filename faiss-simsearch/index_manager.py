import numpy as np
from faiss_index import build_faiss_index
from embedding import get_embedding
from function_extraction import extract_functions
from preprocessing import preprocess
from submission_store import store_submission, get_all_embeddings_for_question
from config import SIMILARITY_THRESHOLD, TOP_K

index_cache = {}

def add_submission(user_id, question_id, code):
    processed = preprocess(code)
    functions = extract_functions(processed)

    for fn in functions:
        if len(fn['code'].splitlines()) < 4:
            continue
        embedding = get_embedding(fn['code'])
        if not np.all(np.isfinite(embedding)) or np.linalg.norm(embedding) == 0:
            continue
        store_submission(question_id, user_id, embedding, fn['code'])

    if question_id in index_cache:
        del index_cache[question_id]

def find_similar_submissions(question_id, code):
    processed = preprocess(code)
    functions = extract_functions(processed)

    query_embeddings = []
    for fn in functions:
        if len(fn['code'].splitlines()) < 4:
            continue
        embedding = get_embedding(fn['code'])
        if np.all(np.isfinite(embedding)) and np.linalg.norm(embedding) > 0:
            query_embeddings.append(embedding)

    if not query_embeddings:
        return []

    stored = get_all_embeddings_for_question(question_id)
    if not stored:
        return []

    all_embeddings = np.array([s["embedding"] for s in stored]).astype('float32')

    if question_id not in index_cache:
        index, _ = build_faiss_index(all_embeddings)
        index_cache[question_id] = (index, stored)

    index, stored_data = index_cache[question_id]
    query = np.array(query_embeddings).astype('float32')
    D, I = index.search(query, k=TOP_K)

    similar_submissions = []
    for distances, indices in zip(D, I):
        for dist, idx in zip(distances, indices):
            if dist >= SIMILARITY_THRESHOLD:
                match = stored_data[idx]
                similar_submissions.append({
                    "userID": match["userID"],
                    "code": match["code"]
                })

    return similar_submissions

