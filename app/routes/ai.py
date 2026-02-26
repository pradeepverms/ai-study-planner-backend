from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.logic.ai_engine import generate_explanation
from app.logic.monetization import can_use_feature

router = APIRouter(
    prefix="/ai",
    tags=["AI Tutor"]
)

# TEMP: hardcoded user (later from auth)
USER_PLAN = "FREE"
AI_USED_TODAY = 2


class AIRequest(BaseModel):
    question: str
    topic: str
    correct_answer: str
    user_answer: str


@router.post("/explain")
def explain(payload: AIRequest):
    if not can_use_feature(USER_PLAN, "daily_ai_calls", AI_USED_TODAY):
        raise HTTPException(
            status_code=403,
            detail="Daily AI limit reached. Upgrade to PRO."
        )

    return generate_explanation(
        question=payload.question,
        correct_answer=payload.correct_answer,
        user_answer=payload.user_answer,
        topic=payload.topic
    )