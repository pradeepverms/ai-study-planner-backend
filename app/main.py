from fastapi import FastAPI
from app.routes import planner, feedback, adaptive

app = FastAPI(title="AI Study Planner")

app.include_router(planner.router)
app.include_router(feedback.router)
app.include_router(adaptive.router)

@app.get("/")
def root():
    return {"message": "AI Study Planner with Adaptive Intelligence Running"}