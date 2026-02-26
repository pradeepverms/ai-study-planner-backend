from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import PlannerState, Feedback

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("/submit")
def submit_feedback(payload: dict, db: Session = Depends(get_db)):
    state = db.query(PlannerState).first()

    if not state:
        return {"error": "Planner not initialized"}

    accuracy = payload["accuracy"]

    # --- Adaptive rules ---
    if accuracy > 75:
        adjustment = "increase_difficulty"
        state.daily_hours = min(state.daily_hours + 1, 6)
        state.difficulty = "hard"
    elif accuracy < 50:
        adjustment = "decrease_difficulty"
        state.daily_hours = max(state.daily_hours - 1, 2)
        state.difficulty = "easy"
    else:
        adjustment = "maintain"
        state.difficulty = "medium"

    state.day += 1

    feedback = Feedback(
        day=state.day - 1,
        completed=payload["completed"],
        accuracy=accuracy,
        time_spent=payload["time_spent"]
    )

    db.add(feedback)
    db.commit()

    return {
        "day": state.day - 1,
        "adaptive_response": {
            "adjustment": adjustment,
            "next_day_hours": state.daily_hours,
            "reason": "Adaptive update based on performance"
        }
    }