from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date
from typing import List
import math

app = FastAPI(title="AI Study Planner Backend v2")

# -------------------- MODELS --------------------

class PlanRequest(BaseModel):
    exam: str
    exam_date: date
    daily_hours: int
    level: str
    topics: List[str]


class SubTopic(BaseModel):
    name: str
    duration_minutes: int
    activity: str
    confidence: float


class TopicPlan(BaseModel):
    topic: str
    total_hours: int
    subtopics: List[SubTopic]


class PlanResponse(BaseModel):
    exam: str
    days_left: int
    mode: str
    daily_plan: List[TopicPlan]


# -------------------- INTELLIGENCE --------------------

SUBTOPIC_MAP = {
    "calculus": [
        "limits",
        "continuity",
        "differentiation",
        "applications_of_derivatives",
        "integration"
    ],
    "probability": [
        "basic_probability",
        "conditional_probability",
        "bayes_theorem",
        "random_variables"
    ]
}

ACTIVITY_MAP = {
    "beginner": "concept building + solved examples",
    "intermediate": "problem solving + PYQs",
    "advanced": "mixed PYQs + mock analysis"
}


def calculate_confidence(level: str, subtopic_index: int) -> float:
    base = {
        "beginner": 0.35,
        "intermediate": 0.55,
        "advanced": 0.75
    }.get(level, 0.4)

    decay = subtopic_index * 0.05
    return round(max(base - decay, 0.2), 2)


# -------------------- ROUTES --------------------

@app.get("/api/v1/health")
def health():
    return {"status": "ok", "env": "production"}


@app.post("/api/v1/generate-plan", response_model=PlanResponse)
def generate_plan(req: PlanRequest):
    today = date.today()
    days_left = (req.exam_date - today).days

    mode = "normal"
    if days_left < 60:
        mode = "panic"
    elif days_left < 120:
        mode = "intensive"

    daily_plan = []

    minutes_per_day = req.daily_hours * 60

    for topic in req.topics:
        subtopics = SUBTOPIC_MAP.get(topic.lower(), ["general_revision"])
        minutes_per_subtopic = math.floor(minutes_per_day / len(subtopics))

        structured_subtopics = []

        for idx, sub in enumerate(subtopics):
            structured_subtopics.append(
                SubTopic(
                    name=sub,
                    duration_minutes=minutes_per_subtopic,
                    activity=ACTIVITY_MAP.get(req.level, "revision"),
                    confidence=calculate_confidence(req.level, idx)
                )
            )

        daily_plan.append(
            TopicPlan(
                topic=topic,
                total_hours=req.daily_hours,
                subtopics=structured_subtopics
            )
        )

    return PlanResponse(
        exam=req.exam,
        days_left=days_left,
        mode=mode,
        daily_plan=daily_plan
    )