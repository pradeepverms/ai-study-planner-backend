from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from datetime import datetime
from app.database import Base

class StudyPlan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    exam = Column(String)
    level = Column(String)
    daily_hours = Column(Integer)
    difficulty = Column(String)
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class DailyProgress(Base):
    __tablename__ = "daily_progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    day = Column(Integer)
    completed = Column(Boolean)
    accuracy = Column(Integer)
    time_spent = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

class AdaptiveDecision(Base):
    __tablename__ = "adaptive_decisions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    window = Column(String)
    adjustment = Column(String)
    reason = Column(String)
    next_day_hours = Column(Integer)
    difficulty = Column(String)
    confidence = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Streak(Base):
    __tablename__ = "streaks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    current = Column(Integer, default=0)
    best = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow)