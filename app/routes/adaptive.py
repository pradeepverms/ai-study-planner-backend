from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/adaptive", tags=["Adaptive"])

class FeedbackInput(BaseModel):
    day: int
    completed: bool
    accuracy: int   # 0 - 100
    time_spent: int # minutes

class AdaptiveResponse(BaseModel):
    adjustment: str
    next_day_hours: int
    reason: str

@router.post("/evaluate", response_model=AdaptiveResponse)
def evaluate_feedback(feedback: FeedbackInput):

    # Default values
    adjustment = "keep_same"
    next_day_hours = 4
    reason = "Stable performance."

    # Rule 1: Not completed
    if not feedback.completed:
        adjustment = "force_revision"
        next_day_hours = 2
        reason = "Task not completed. Reducing load and enforcing revision."
        return AdaptiveResponse(
            adjustment=adjustment,
            next_day_hours=next_day_hours,
            reason=reason
        )

    # Rule 2: Very low accuracy
    if feedback.accuracy < 40:
        adjustment = "decrease_difficulty"
        next_day_hours = max(2, feedback.time_spent // 60)
        reason = "Low accuracy detected. Reducing difficulty to rebuild fundamentals."
        return AdaptiveResponse(
            adjustment=adjustment,
            next_day_hours=next_day_hours,
            reason=reason
        )

    # Rule 3: High accuracy + low time
    if feedback.accuracy >= 80 and feedback.time_spent <= 90:
        adjustment = "increase_difficulty"
        next_day_hours = min(6, feedback.time_spent // 60 + 1)
        reason = "High accuracy with low time. Increasing challenge level."
        return AdaptiveResponse(
            adjustment=adjustment,
            next_day_hours=next_day_hours,
            reason=reason
        )

    # Rule 4: High effort but medium accuracy
    if feedback.accuracy >= 60 and feedback.time_spent >= 180:
        adjustment = "keep_same"
        next_day_hours = feedback.time_spent // 60
        reason = "Good effort but moderate accuracy. Maintaining current difficulty."
        return AdaptiveResponse(
            adjustment=adjustment,
            next_day_hours=next_day_hours,
            reason=reason
        )

    return AdaptiveResponse(
        adjustment=adjustment,
        next_day_hours=next_day_hours,
        reason=reason
    )