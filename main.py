from fastapi import FastAPI
from schemas import PlanRequest, PlanResponse
from planner import generate_plan

app = FastAPI(
    title="AI Study Planner Backend-2",
    version="2.0",
    description="Adaptive + Panic-Aware + Confidence-Driven Study Planner"
)


@app.get("/api/v1/health")
def health():
    return {"status": "ok", "env": "production"}


@app.post("/api/v1/generate-plan", response_model=PlanResponse)
def create_plan(payload: PlanRequest):
    return generate_plan(payload)