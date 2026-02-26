from fastapi import FastAPI

from app.routes.exam import router as exam_router
from app.routes.planner import router as planner_router
from app.routes.questions import router as question_router
from app.routes.feedback import router as feedback_router
from app.routes.adaptive import router as adaptive_router
from app.routes.ai import router as ai_router
from app.routes.billing import router as billing_router

app = FastAPI(
    title="Adaptive AI Study Planner",
    version="3.0.0"
)

@app.get("/")
def root():
    return {"message": "AI Study Planner with Monetization Running"}

app.include_router(exam_router)
app.include_router(planner_router)
app.include_router(question_router)
app.include_router(feedback_router)
app.include_router(adaptive_router)
app.include_router(ai_router)
app.include_router(billing_router)