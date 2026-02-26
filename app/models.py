from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.database import Base

class StudyPlan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    exam = Column(String)
    level = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class DailyProgress(Base):
    __tablename__ = "daily_progress"

    id = Column(Integer, primary_key=True, index=True)
    day = Column(Integer)
    completed = Column(Boolean)
    accuracy = Column(Integer)
    time_spent = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)


class AdaptiveDecision(Base):
    __tablename__ = "adaptive_decisions"

    id = Column(Integer, primary_key=True, index=True)
    day = Column(Integer)
    adjustment = Column(String)
    reason = Column(String)
    next_day_hours = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)