from pydantic import BaseModel, Field
from typing import List, Dict


class PlanRequest(BaseModel):
    exam: str = Field(..., example="GATE DA")
    exam_date: str = Field(..., example="2028-02-08")
    daily_hours: int = Field(..., ge=1, le=12)
    level: str = Field(..., example="beginner")
    topics: List[str]


class Activity(BaseModel):
    topic: str
    subtopic: str
    duration_hours: float
    activity: str
    confidence: float


class DailyPlan(BaseModel):
    day: int
    total_hours: float
    activities: List[Activity]


class PlanResponse(BaseModel):
    exam: str
    days_left: int
    mode: str
    daily_plan: List[DailyPlan]