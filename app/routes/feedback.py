from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import DailyProgress, AdaptiveDecision, StudyPlan, Streak

router = APIRouter(prefix="/feedback", tags=["Feedback"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/submit")
def submit_feedback(payload: dict, db: Session = Depends(get_db)):
    user_id = payload["user_id"]
    day = payload["day"]
    completed = payload["completed"]
    accuracy = payload["accuracy"]
    time_spent = payload["time_spent"]

    db.add(DailyProgress(
        user_id=user_id, day=day, completed=completed,
        accuracy=accuracy, time_spent=time_spent
    ))

    plan = db.query(StudyPlan).filter_by(user_id=user_id).first()
    if not plan:
        return {"error": "Planner not initialized"}

    streak = db.query(Streak).filter_by(user_id=user_id).first()
    if not streak:
        streak = Streak(user_id=user_id, current=0, best=0)
        db.add(streak)

    if completed:
        streak.current += 1
        streak.best = max(streak.best, streak.current)
    else:
        streak.current = 0

    if not completed:
        adjustment, reason, conf = "force_revision", "Task incomplete", 0.8
        plan.daily_hours = max(2, plan.daily_hours - 1)
        plan.difficulty = "easy"
    elif accuracy >= 90 and time_spent <= plan.daily_hours * 60:
        adjustment, reason, conf = "increase_difficulty", "Excellent efficiency", 0.9
        plan.daily_hours = min(6, plan.daily_hours + 1)
        plan.difficulty = "hard"
    elif accuracy < 50:
        adjustment, reason, conf = "decrease_difficulty", "Low accuracy", 0.85
        plan.daily_hours = max(2, plan.daily_hours - 1)
        plan.difficulty = "easy"
    else:
        adjustment, reason, conf = "keep_same", "Stable day", 0.6

    db.add(AdaptiveDecision(
        user_id=user_id,
        window="daily",
        adjustment=adjustment,
        reason=reason,
        next_day_hours=plan.daily_hours,
        difficulty=plan.difficulty,
        confidence=conf
    ))

    db.commit()

    return {
        "day": day,
        "adaptive_response": {
            "adjustment": adjustment,
            "next_day_hours": plan.daily_hours,
            "difficulty": plan.difficulty,
            "reason": reason,
            "confidence": conf
        },
        "streak": {"current": streak.current, "best": streak.best}
    }