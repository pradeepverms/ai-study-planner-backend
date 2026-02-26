from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import PlannerState

router = APIRouter(prefix="/planner", tags=["Planner"])


@router.post("/generate")
def generate_plan(payload: dict, db: Session = Depends(get_db)):
    exam_name = payload["exam_name"]
    level = payload["level"]

    state = db.query(PlannerState).first()

    if not state:
        state = PlannerState(
            exam_name=exam_name,
            level=level,
            daily_hours=payload["daily_hours"],
            difficulty="medium",
            day=1
        )
        db.add(state)
        db.commit()
        db.refresh(state)

    plan = {
        "day": state.day,
        "daily_hours": state.daily_hours,
        "difficulty": state.difficulty,
        "topics": ["Core Concepts", "Practice Questions"],
        "practice_questions": state.daily_hours * 10
    }

    return {
        "exam": state.exam_name,
        "level": state.level,
        "plan": plan
    }