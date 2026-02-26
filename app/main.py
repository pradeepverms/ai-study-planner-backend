from fastapi import FastAPI
from database import Base, engine
from routes import planner, feedback

app = FastAPI(title="AI Study Planner")

Base.metadata.create_all(bind=engine)

app.include_router(planner.router)
app.include_router(feedback.router)


@app.get("/")
def root():
    return {"message": "AI Study Planner Running"}