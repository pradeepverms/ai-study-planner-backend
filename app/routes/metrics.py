from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from statistics import mean
from app.database import SessionLocal
from app.models import DailyProgress, AdaptiveDecision, Streak

router = APIRouter(prefix="/metrics", tags=["Metrics"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/overview")
def metrics_overview(user_id: str, db: Session = Depends(get_db)):
    progress = db.query(DailyProgress).filter_by(user_id=user_id).all()
    decisions = db.query(AdaptiveDecision).filter_by(user_id=user_id).all()
    streak = db.query(Streak).filter_by(user_id=user_id).first()

    if not progress:
        return {"message": "No data yet"}

    accuracy_avg = mean([p.accuracy for p in progress])
    completion_rate = sum(1 for p in progress if p.completed) / len(progress)
    confidence_avg = mean([d.confidence for d in decisions]) if decisions else 0

    return {
        "signals": {
            "accuracy_avg": round(accuracy_avg, 1),
            "completion_rate": round(completion_rate, 2),
            "confidence_avg": round(confidence_avg, 2),
        },
        "streak": {
            "current": streak.current if streak else 0,
            "best": streak.best if streak else 0
        },
        "insight": (
            "Consistency is driving improvement"
            if completion_rate >= 0.7 else
            "Inconsistent study is limiting progress"
        )
    }