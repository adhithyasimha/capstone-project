from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from index_manager import add_submission, find_similar_submissions

app = FastAPI()

class SubmissionPayload(BaseModel):
    userID: str
    questionID: str
    code: str

@app.put("/submission")
def put_submission(payload: SubmissionPayload):
    try:
        add_submission(payload.userID, payload.questionID, payload.code)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/submission")
def get_submission(questionID: str = Query(...), code: str = Query(...)):
    try:
        similar = find_similar_submissions(questionID, code)
        print(similar)
        if not similar:
            return {"found": False}
        return {
            "found": True,
            "similarSubmissions": similar
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

