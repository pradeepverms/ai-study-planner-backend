from pydantic import BaseModel, Field
from typing import List
from datetime import date


class PlanRequest(BaseModel):
    exam: str = Field(..., example="GATE DA")
    exam_date: date
    daily_hours: int = Field(..., ge=1, le=16)
    level: str = Field(..., example="beginner")
    topics: List[str]


class DailySlot(BaseModel):
    topic: str
    duration: str
    type: str


class DayPlan(BaseModel):
    day: int
    focus: str
    schedule: List[DailySlot]


class PlanResponse(BaseModel):
    exam: str
    days_left: int
    mode: str
    plan: List[DayPlan]
    revision_strategy: dict