from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.planner import router as planner_router
from app.routes.feedback import router as feedback_router

app = FastAPI(title="AI Study Planner")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "AI Study Planner Backend Running"}

# Routes
app.include_router(planner_router, prefix="/planner", tags=["Planner"])
app.include_router(feedback_router, prefix="/feedback", tags=["Feedback"])