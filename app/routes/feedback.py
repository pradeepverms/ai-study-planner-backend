from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import DailyProgress, AdaptiveDecision

router = APIRouter(prefix="/feedback", tags=["Feedback"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/submit")
def submit_feedback(payload: dict, db: Session = Depends(get_db)):
    day = payload["day"]
    completed = payload["completed"]
    accuracy = payload["accuracy"]
    time_spent = payload["time_spent"]

    progress = DailyProgress(
        day=day,
        completed=completed,
        accuracy=accuracy,
        time_spent=time_spent
    )
    db.add(progress)

    if accuracy >= 80:
        adjustment = "increase_difficulty"
        next_hours = time_spent + 10
        reason = "High accuracy, increasing challenge"
    elif accuracy < 50:
        adjustment = "decrease_difficulty"
        next_hours = max(30, time_spent - 10)
        reason = "Low accuracy, reducing load"
    else:
        adjustment = "keep_same"
        next_hours = time_spent
        reason = "Balanced performance"

    decision = AdaptiveDecision(
        day=day,
        adjustment=adjustment,
        reason=reason,
        next_day_hours=next_hours
    )

    db.add(decision)
    db.commit()

    return {
        "day": day,
        "adaptive_response": {
            "adjustment": adjustment,
            "next_day_hours": next_hours,
            "reason": reason
        }
    }