from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from statistics import mean
from app.database import SessionLocal
from app.models import DailyProgress, AdaptiveDecision, StudyPlan, Streak

router = APIRouter(prefix="/reports", tags=["Reports"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/weekly")
def weekly_report(db: Session = Depends(get_db)):
    plan = db.query(StudyPlan).first()
    if not plan:
        return {"error": "Planner not initialized"}

    if not plan.is_premium:
        raise HTTPException(status_code=403, detail="Premium feature")

    last7 = (
        db.query(DailyProgress)
        .order_by(DailyProgress.timestamp.desc())
        .limit(7)
        .all()
    )

    if not last7:
        return {"message": "No data yet"}

    acc_avg = mean([d.accuracy for d in last7])
    time_avg = mean([d.time_spent for d in last7])
    completion_rate = sum(1 for d in last7 if d.completed) / len(last7)

    decisions = (
        db.query(AdaptiveDecision)
        .order_by(AdaptiveDecision.timestamp.desc())
        .limit(7)
        .all()
    )

    confidence_avg = mean([d.confidence for d in decisions]) if decisions else 0

    streak = db.query(Streak).first()

    burnout_risk = "low"
    if acc_avg < 65 and time_avg > plan.daily_hours * 60:
        burnout_risk = "high"
    elif acc_avg < 70:
        burnout_risk = "medium"

    return {
        "summary": {
            "accuracy_avg": round(acc_avg, 1),
            "time_spent_avg_min": int(time_avg),
            "completion_rate": round(completion_rate, 2),
            "confidence_avg": round(confidence_avg, 2),
            "burnout_risk": burnout_risk
        },
        "streak": {
            "current": streak.current if streak else 0,
            "best": streak.best if streak else 0
        },
        "recommendation": (
            "Maintain pace" if burnout_risk == "low"
            else "Reduce load and revise fundamentals"
        )
    }