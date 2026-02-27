from pydantic import BaseModel, Field
from typing import List


class PlanRequest(BaseModel):
    exam: str = Field(..., example="GATE DA")
    exam_date: str = Field(..., example="2028-02-08")
    daily_hours: int = Field(..., ge=1, le=12, example=4)
    level: str = Field(..., example="beginner")
    topics: List[str] = Field(..., example=["calculus"])


class SubTopicPlan(BaseModel):
    name: str
    duration_minutes: int
    activity: str
    confidence: float


class TopicPlan(BaseModel):
    topic: str
    total_hours: int
    subtopics: List[SubTopicPlan]


class PlanResponse(BaseModel):
    exam: str
    days_left: int
    mode: str
    daily_plan: List[TopicPlan]