from fastapi import APIRouter
from pydantic import BaseModel
from app.routes.adaptive import evaluate_feedback, FeedbackInput

router = APIRouter(prefix="/feedback", tags=["Feedback"])

class FeedbackRequest(BaseModel):
    day: int
    completed: bool
    accuracy: int
    time_spent: int

@router.post("/submit")
def submit_feedback(feedback: FeedbackRequest):

    adaptive_result = evaluate_feedback(
        FeedbackInput(
            day=feedback.day,
            completed=feedback.completed,
            accuracy=feedback.accuracy,
            time_spent=feedback.time_spent
        )
    )

    return {
        "day": feedback.day,
        "adaptive_response": adaptive_result
    }