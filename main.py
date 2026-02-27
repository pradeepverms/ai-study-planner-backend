from fastapi import FastAPI
from schemas import PlanRequest, PlanResponse
from planner import generate_plan

app = FastAPI(title="AI Study Planner", version="2.1")


@app.get("/api/v1/health")
def health():
    return {"status": "ok", "env": "production"}


@app.post("/api/v1/generate-plan", response_model=PlanResponse)
def generate_study_plan(req: PlanRequest):
    days_left, mode, plan = generate_plan(
        req.exam,
        req.exam_date,
        req.daily_hours,
        req.level,
        req.topics,
    )

    return PlanResponse(
        exam=req.exam,
        days_left=days_left,
        mode=mode,
        daily_plan=plan,
    )