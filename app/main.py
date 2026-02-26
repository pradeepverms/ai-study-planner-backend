from fastapi import FastAPI
from app.routes.planner import router as planner_router
from app.routes.feedback import router as feedback_router

app = FastAPI(title="AI Study Planner")

app.include_router(planner_router)
app.include_router(feedback_router)

@app.get("/")
def root():
    return {"message": "AI Study Planner with Monetization Running"}