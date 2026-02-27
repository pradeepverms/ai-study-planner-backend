from fastapi import FastAPI
from schemas import PlanRequest, PlanResponse
from planner import generate_plan

app = FastAPI(
    title="AI Study Planner",
    version="2.0",
    description="Deterministic, intelligence-driven study planner engine"
)


@app.get("/api/v1/health")
def health():
    return {"status": "ok", "env": "production"}


@app.post("/api/v1/generate-plan", response_model=PlanResponse)
def generate_study_plan(payload: PlanRequest):
    return generate_plan(payload)