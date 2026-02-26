from fastapi import FastAPI
from app.routes.planner import router as planner_router
from app.routes.feedback import router as feedback_router

app = FastAPI(
    title="AI Study Planner",
    description="Adaptive AI-powered study planner backend",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "AI Study Planner Backend Running"}

app.include_router(planner_router)
app.include_router(feedback_router)