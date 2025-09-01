from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import logging
from index_manager import add_submission, find_similar_submissions

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

class SubmissionPayload(BaseModel):
    userID: str
    questionID: str
    code: str

@app.put("/submission")
def put_submission(payload: SubmissionPayload):
    logger.info(f"PUT /submission - userID: {payload.userID}, questionID: {payload.questionID}")
    logger.info(f"Code length: {len(payload.code)}")
    
    try:
        add_submission(payload.userID, payload.questionID, payload.code)
        logger.info("Submission added successfully")
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error adding submission: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/submission")
def get_submission(questionID: str = Query(...), code: str = Query(...)):
    logger.info(f"GET /submission - questionID: {questionID}")
    logger.info(f"Query code length: {len(code)}")
    
    try:
        similar = find_similar_submissions(questionID, code)
        logger.info(f"Found {len(similar)} similar submissions")
        
        if not similar:
            logger.info("No similar submissions found, returning found=false")
            return {"found": False}
        
        logger.info(f"Returning {len(similar)} similar submissions")
        return {
            "found": True,
            "similarSubmissions": similar
        }
    except Exception as e:
        logger.error(f"Error finding similar submissions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

