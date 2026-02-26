from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.logic.feedback_engine import evaluate_exam

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback Engine"]
)


class AnswerSubmission(BaseModel):
    question_id: int
    topic: str
    correct_answer: str
    user_answer: str


class FeedbackRequest(BaseModel):
    submissions: List[AnswerSubmission]


@router.post("/evaluate")
def evaluate(payload: FeedbackRequest):
    result = evaluate_exam([s.dict() for s in payload.submissions])
    return result