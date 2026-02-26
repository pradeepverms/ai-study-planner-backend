from fastapi import FastAPI
from app.routes.planner import router as planner_router

app = FastAPI(title="AI Study Planner")

@app.get("/")
def root():
    return {
        "message": "AI Study Planner Backend Running"
    }

app.include_router(planner_router)