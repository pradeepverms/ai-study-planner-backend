from fastapi import FastAPI
from app.routes.planner import router as planner_router

app = FastAPI(
    title="AI Study Planner",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "AI Study Planner Backend Running"
    }

# VERY IMPORTANT LINE
app.include_router(planner_router)