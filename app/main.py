from fastapi import FastAPI
from app.database import Base, engine
from app.routes import planner, feedback

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Study Planner", version="2.0")

app.include_router(planner.router)
app.include_router(feedback.router)

@app.get("/")
def root():
    return {"message": "AI Study Planner v2 Running"}