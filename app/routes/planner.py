from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date
from math import ceil

router = APIRouter(prefix="/planner", tags=["Planner"])

class PlannerRequest(BaseModel):
    exam_name: str
    exam_date: date
    daily_hours: int
    level: str  # beginner / intermediate / advanced

@router.post("/generate")
def generate_plan(data: PlannerRequest):
    today = date.today()
    days_left = (data.exam_date - today).days

    if days_left <= 0:
        return {"error": "Exam date must be in the future"}

    topics = [
        "Limits",
        "Continuity",
        "Differentiation",
        "Applications of Derivatives",
        "Integration",
        "Definite Integrals",
        "Differential Equations"
    ]

    topics_per_day = ceil(len(topics) / days_left)
    plan = []

    index = 0
    for day in range(days_left):
        day_topics = topics[index:index + topics_per_day]
        index += topics_per_day

        plan.append({
            "day": day + 1,
            "study_hours": data.daily_hours,
            "topics": day_topics,
            "practice_questions": len(day_topics) * 10
        })

        if index >= len(topics):
            break

    return {
        "exam": data.exam_name,
        "level": data.level,
        "days_left": days_left,
        "daily_plan": plan
    }