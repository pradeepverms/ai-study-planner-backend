from fastapi import APIRouter
from pydantic import BaseModel
from app.logic.adaptive_engine import analyze_feedback

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"]
)

class FeedbackRequest(BaseModel):
    day: int
    completed: bool
    accuracy: int
    time_spent: int

@router.post("/submit")
def submit_feedback(payload: FeedbackRequest):
    adjustment = analyze_feedback(payload.dict())
    return {
        "day": payload.day,
        "adaptive_response": adjustment
    }