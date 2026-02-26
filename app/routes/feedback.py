from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

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
    adjustment = "keep_same"

    if payload.accuracy < 70:
        adjustment = "increase_practice"
    elif payload.accuracy > 90:
        adjustment = "increase_difficulty"

    return {
        "day": payload.day,
        "adjustment": adjustment,
        "next_day_hours": payload.time_spent + 1 if adjustment != "keep_same" else payload.time_spent,
        "timestamp": datetime.utcnow().isoformat()
    }