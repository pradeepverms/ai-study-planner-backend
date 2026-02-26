from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from statistics import mean, pstdev

from app.database import SessionLocal
from app.models import StudyPlan, DailyProgress, AdaptiveDecision

router = APIRouter(prefix="/planner", tags=["Planner"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

TOPICS = ["Limits", "Continuity", "Differentiation", "Integration", "Matrices"]

@router.post("/generate")
def generate_plan(payload: dict, db: Session = Depends(get_db)):
    exam = payload["exam_name"]
    level = payload["level"]
    exam_date = date.fromisoformat(payload["exam_date"])
    base_hours = payload["daily_hours"]

    days_left = (exam_date - date.today()).days
    if days_left <= 0:
        return {"error": "Exam date must be in the future"}

    plan = db.query(StudyPlan).first()
    if not plan:
        plan = StudyPlan(
            exam=exam,
            level=level,
            daily_hours=base_hours,
            difficulty="medium",
            is_premium=False
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)

    # Weekly intelligence (last 7 days)
    last7 = (
        db.query(DailyProgress)
        .order_by(DailyProgress.timestamp.desc())
        .limit(7)
        .all()
    )

    adj = None
    if len(last7) >= 3:
        accs = [d.accuracy for d in last7]
        times = [d.time_spent for d in last7]
        acc_avg = mean(accs)
        acc_var = pstdev(accs) if len(accs) > 1 else 0

        # Burnout: accuracy down + time up
        if acc_avg < 65 and mean(times) > plan.daily_hours * 60:
            plan.daily_hours = max(2, plan.daily_hours - 1)
            plan.difficulty = "easy"
            adj = ("burnout", "Accuracy dropping with high effort", 0.85)

        # Acceleration: accuracy high + stable
        elif acc_avg >= 80 and acc_var < 8:
            plan.daily_hours = min(6, plan.daily_hours + 1)
            plan.difficulty = "hard"
            adj = ("accelerate", "Consistently high accuracy", 0.9)

        # Avoidance: accuracy down + time down
        elif acc_avg < 60 and mean(times) < plan.daily_hours * 40:
            plan.daily_hours = max(2, plan.daily_hours - 1)
            plan.difficulty = "easy"
            adj = ("avoidance", "Low effort and low accuracy", 0.75)

        if adj:
            decision = AdaptiveDecision(
                window="weekly",
                adjustment=adj[0],
                reason=adj[1],
                next_day_hours=plan.daily_hours,
                difficulty=plan.difficulty,
                confidence=adj[2]
            )
            db.add(decision)
            db.commit()

    # Build next 5-day plan
    daily_plan = []
    for i in range(1, 6):
        daily_plan.append({
            "day": i,
            "study_hours": plan.daily_hours,
            "difficulty": plan.difficulty,
            "topics": [TOPICS[(i - 1) % len(TOPICS)]],
            "practice_questions": plan.daily_hours * (8 if plan.difficulty == "easy" else 10)
        })

    db.commit()

    return {
        "exam": plan.exam,
        "level": plan.level,
        "days_left": days_left,
        "difficulty": plan.difficulty,
        "daily_plan": daily_plan
    }