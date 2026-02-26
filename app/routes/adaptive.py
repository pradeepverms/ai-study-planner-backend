from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date
import json

from app.logic.adaptive_engine import generate_adaptive_plan

router = APIRouter(
    prefix="/adaptive",
    tags=["Adaptive Planner"]
)


class AdaptiveRequest(BaseModel):
    exam_date: date
    weak_topics: list


@router.post("/generate")
def generate(payload: AdaptiveRequest):
    with open("app/data/calculus_topics.json", "r") as f:
        topics = json.load(f)["topics"]

    return generate_adaptive_plan(
        exam_date=payload.exam_date,
        topics=topics,
        weak_topics=payload.weak_topics
    )