from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date

router = APIRouter(
    prefix="/exam",
    tags=["Exam"]
)

class ExamSetupRequest(BaseModel):
    name: str
    exam_date: date

@router.post("/setup")
def setup_exam(payload: ExamSetupRequest):
    return {
        "status": "success",
        "exam_name": payload.name,
        "exam_date": payload.exam_date
    }