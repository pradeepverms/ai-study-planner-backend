from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date
import json

from app.logic.roadmap import generate_daily_plan

router = APIRouter(
    prefix="/planner",
    tags=["Planner"]
)

class PlannerRequest(BaseModel):
    exam_date: date

@router.post("/generate")
def generate_plan(payload: PlannerRequest):
    with open("app/data/calculus_topics.json", "r") as f:
        topics = json.load(f)

    return generate_daily_plan(
        exam_date=payload.exam_date,
        topics=topics
    )