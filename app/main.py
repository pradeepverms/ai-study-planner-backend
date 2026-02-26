from fastapi import FastAPI
from app.database import Base, engine
from app.routes import planner, feedback
from app.routes.reports import router as reports_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Study Planner", version="4.0")

app.include_router(planner.router)
app.include_router(feedback.router)
app.include_router(reports_router)

@app.get("/")
def root():
    return {"message": "AI Study Planner v4 Running"}