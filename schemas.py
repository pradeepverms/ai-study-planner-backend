from pydantic import BaseModel, Field
from typing import List
from datetime import date


class PlanRequest(BaseModel):
    exam: str = Field(..., example="GATE DA")
    exam_date: date = Field(..., example="2028-02-05")
    daily_hours: int = Field(..., gt=0, le=12)
    level: str = Field(..., example="beginner")
    topics: List[str] = Field(..., example=["math"])


class DailyPlanItem(BaseModel):
    topic: str
    subtopic: str
    duration_hours: float
    activity: str
    confidence: float | None = None


class PlanResponse(BaseModel):
    exam: str
    days_left: int
    mode: str
    daily_plan: List[DailyPlanItem]