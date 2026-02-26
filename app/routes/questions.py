from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import json
import random

router = APIRouter(
    prefix="/questions",
    tags=["Question Engine"]
)

DATA_PATH = "app/data/calculus_questions.json"


class QuestionRequest(BaseModel):
    topic: str
    count: int = 5


@router.post("/generate")
def generate_questions(payload: QuestionRequest):
    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    if payload.topic not in data:
        return {"error": "Topic not found"}

    questions = data[payload.topic]
    selected = random.sample(
        questions,
        min(payload.count, len(questions))
    )

    return {
        "topic": payload.topic,
        "questions": selected
    }