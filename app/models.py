from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class PlannerState(Base):
    __tablename__ = "planner_state"

    id = Column(Integer, primary_key=True, index=True)
    exam_name = Column(String, index=True)
    level = Column(String)
    daily_hours = Column(Integer)
    difficulty = Column(String)
    day = Column(Integer, default=1)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    day = Column(Integer)
    completed = Column(Boolean)
    accuracy = Column(Integer)
    time_spent = Column(Integer)