from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, date

from app.database import SessionLocal
from app.models import StudyPlan, DailyProgress, AdaptiveDecision

router = APIRouter(prefix="/planner", tags=["Planner"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/generate")
def generate_plan(payload: dict, db: Session = Depends(get_db)):
    exam = payload["exam_name"]
    level = payload["level"]
    exam_date = date.fromisoformat(payload["exam_date"])
    daily_hours = payload["daily_hours"]

    days_left = (exam_date - date.today()).days
    if days_left <= 0:
        return {"error": "Exam date must be in the future"}

    plan = StudyPlan(exam=exam, level=level)
    db.add(plan)
    db.commit()

    topics = ["Limits", "Continuity", "Differentiation", "Integration", "Matrices"]
    daily_plan = []

    for i in range(1, 6):
        daily_plan.append({
            "day": i,
            "study_hours": daily_hours,
            "topics": [topics[(i - 1) % len(topics)]],
            "practice_questions": 10
        })

    return {
        "exam": exam,
        "level": level,
        "days_left": days_left,
        "daily_plan": daily_plan
    }