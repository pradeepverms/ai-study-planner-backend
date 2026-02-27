from pydantic import BaseModel
from typing import List
from datetime import date


class PlanRequest(BaseModel):
    exam: str
    exam_date: date
    daily_hours: int
    level: str
    topics: List[str]


class DailyPlanItem(BaseModel):
    topic: str
    subtopic: str
    duration_hours: float
    activity: str
    confidence: float | None


class PlanResponse(BaseModel):
    exam: str
    days_left: int
    mode: str
    daily_plan: List[DailyPlanItem]