import os
import pickle

SAVE_DIR = "./saved_data"
SAVE_PATH = os.path.join(SAVE_DIR, "submissions.pkl")

if os.path.exists(SAVE_PATH):
    with open(SAVE_PATH, "rb") as f:
        submission_db = pickle.load(f)
else:
    submission_db = {}

def persist():
    os.makedirs(SAVE_DIR, exist_ok=True)
    with open(SAVE_PATH, "wb") as f:
        pickle.dump(submission_db, f)

def store_submission(question_id, user_id, embedding, code):
    if question_id not in submission_db:
        submission_db[question_id] = []
    submission_db[question_id].append({
        "userID": user_id,
        "embedding": embedding,
        "code": code
    })
    persist()

def get_all_embeddings_for_question(question_id):
    return submission_db.get(question_id, [])

