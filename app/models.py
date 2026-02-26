from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from datetime import datetime
from app.database import Base

class StudyPlan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True, index=True)
    exam = Column(String)
    level = Column(String)
    daily_hours = Column(Integer)
    difficulty = Column(String)
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class DailyProgress(Base):
    __tablename__ = "daily_progress"
    id = Column(Integer, primary_key=True, index=True)
    day = Column(Integer)
    completed = Column(Boolean)
    accuracy = Column(Integer)
    time_spent = Column(Integer)  # minutes
    timestamp = Column(DateTime, default=datetime.utcnow)

class AdaptiveDecision(Base):
    __tablename__ = "adaptive_decisions"
    id = Column(Integer, primary_key=True, index=True)
    window = Column(String)  # "daily" or "weekly"
    adjustment = Column(String)
    reason = Column(String)
    next_day_hours = Column(Integer)
    difficulty = Column(String)
    confidence = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)