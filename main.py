from fastapi import FastAPI
from schemas import PlanRequest, PlanResponse
from utils import days_left, determine_mode
from planner import build_daily_plan, revision_strategy

app = FastAPI(title="AI Study Planner", version="1.0.0")


@app.get("/api/v1/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/generate-plan", response_model=PlanResponse)
def generate_plan(req: PlanRequest):
    days = days_left(req.exam_date)
    mode = determine_mode(days)

    plan = []
    total_days = min(7, days)  # 7-day rolling plan

    for day in range(1, total_days + 1):
        plan.append(
            build_daily_plan(
                topics=req.topics,
                daily_hours=req.daily_hours,
                day=day
            )
        )

    return PlanResponse(
        exam=req.exam,
        days_left=days,
        mode=mode,
        plan=plan,
        revision_strategy=revision_strategy()
    )