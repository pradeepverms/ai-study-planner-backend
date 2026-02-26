from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import DailyProgress, AdaptiveDecision, StudyPlan

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

    plan = db.query(StudyPlan).first()
    if not plan:
        return {"error": "Planner not initialized"}

    # Daily adaptive rule (capped)
    if not completed:
        adjustment = "force_revision"
        plan.daily_hours = max(2, plan.daily_hours - 1)
        plan.difficulty = "easy"
        reason = "Task incomplete"
        conf = 0.8
    elif accuracy >= 90 and time_spent <= plan.daily_hours * 60:
        adjustment = "increase_difficulty"
        plan.daily_hours = min(6, plan.daily_hours + 1)
        plan.difficulty = "hard"
        reason = "Excellent accuracy with efficient time"
        conf = 0.9
    elif accuracy < 50:
        adjustment = "decrease_difficulty"
        plan.daily_hours = max(2, plan.daily_hours - 1)
        plan.difficulty = "easy"
        reason = "Low accuracy"
        conf = 0.85
    else:
        adjustment = "keep_same"
        reason = "Stable day"
        conf = 0.6

    decision = AdaptiveDecision(
        window="daily",
        adjustment=adjustment,
        reason=reason,
        next_day_hours=plan.daily_hours,
        difficulty=plan.difficulty,
        confidence=conf
    )

    db.add(decision)
    db.commit()

    return {
        "day": day,
        "adaptive_response": {
            "adjustment": adjustment,
            "next_day_hours": plan.daily_hours,
            "difficulty": plan.difficulty,
            "reason": reason,
            "confidence": conf
        }
    }