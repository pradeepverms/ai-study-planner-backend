from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
from typing import List, Dict
import math

app = FastAPI(
    title="AI Study Planner Backend v2",
    version="2.0.0"
)

# -------------------------------
# MODELS
# -------------------------------

class PlanRequest(BaseModel):
    exam: str
    exam_date: date
    daily_hours: int
    level: str
    topics: List[str]

class HourBlock(BaseModel):
    hour: int
    activity: str
    duration_minutes: int
    confidence: float

class TopicPlan(BaseModel):
    topic: str
    subtopic: str
    blocks: List[HourBlock]

class DayPlan(BaseModel):
    day: int
    mode: str
    topics: List[TopicPlan]

class PlanResponse(BaseModel):
    exam: str
    days_left: int
    mode: str
    plan: List[DayPlan]

# -------------------------------
# KNOWLEDGE BASE (EXTENDABLE)
# -------------------------------

SUBTOPIC_MAP = {
    "calculus": [
        "Limits",
        "Continuity",
        "Differentiation",
        "Applications of Derivatives",
        "Integration",
        "Applications of Integrals"
    ],
    "linear algebra": [
        "Matrices",
        "Determinants",
        "Vector Spaces",
        "Eigen Values",
        "Eigen Vectors"
    ],
    "probability": [
        "Random Variables",
        "Distributions",
        "Expectation",
        "Variance",
        "Bayes Theorem"
    ]
}

# -------------------------------
# CORE LOGIC
# -------------------------------

def determine_mode(days_left: int) -> str:
    if days_left <= 30:
        return "panic"
    elif days_left <= 120:
        return "revision"
    return "normal"

def confidence_curve(day: int) -> float:
    # forgetting curve inspired
    base = 90 * math.exp(-0.05 * day)
    return round(max(30, base), 2)

def generate_blocks(hours: int, topic: str, subtopic: str, day: int) -> List[HourBlock]:
    blocks = []
    minutes_per_block = int((hours * 60) / hours)

    for h in range(1, hours + 1):
        blocks.append(
            HourBlock(
                hour=h,
                activity=f"Study {topic} → {subtopic}",
                duration_minutes=minutes_per_block,
                confidence=confidence_curve(day)
            )
        )
    return blocks

# -------------------------------
# API ENDPOINTS
# -------------------------------

@app.get("/api/v1/health")
def health():
    return {"status": "ok", "env": "production"}

@app.post("/api/v1/generate-plan", response_model=PlanResponse)
def generate_plan(req: PlanRequest):

    days_left = (req.exam_date - date.today()).days
    if days_left <= 0:
        raise HTTPException(status_code=400, detail="Exam date must be in the future")

    mode = determine_mode(days_left)

    full_plan: List[DayPlan] = []
    day_counter = 1

    for topic in req.topics:
        subtopics = SUBTOPIC_MAP.get(topic.lower(), ["Core Concepts"])

        for sub in subtopics:
            topic_blocks = generate_blocks(
                req.daily_hours,
                topic,
                sub,
                day_counter
            )

            full_plan.append(
                DayPlan(
                    day=day_counter,
                    mode=mode,
                    topics=[
                        TopicPlan(
                            topic=topic,
                            subtopic=sub,
                            blocks=topic_blocks
                        )
                    ]
                )
            )
            day_counter += 1

    return PlanResponse(
        exam=req.exam,
        days_left=days_left,
        mode=mode,
        plan=full_plan
    )

# -------------------------------
# ROOT (OPTIONAL)
# -------------------------------

@app.get("/")
def root():
    return {
        "message": "AI Study Planner Backend v2 running",
        "docs": "/docs"
    }