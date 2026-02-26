from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, date
from math import exp
import sqlite3
import os

# ===================== ENV =====================
ENV = os.getenv("ENV", "development")
DATABASE_PATH = os.getenv("DATABASE_PATH", "planner.db")

# ===================== APP =====================
app = FastAPI(
    title="AI Study Planner",
    version="1.0.0"
)

# ===================== CORS =====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===================== DATABASE =====================
def db():
    return sqlite3.connect(DATABASE_PATH, check_same_thread=False)

def init_db():
    conn = db()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS topic_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        score INTEGER,
        completed BOOLEAN,
        time_spent INTEGER,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# ===================== MODELS =====================
class PlanRequest(BaseModel):
    exam: str
    exam_date: date
    daily_hours: int
    level: str
    topics: list[str]

class TopicFeedback(BaseModel):
    topic: str
    score: int
    completed: bool
    time_spent: int

# ===================== INTELLIGENCE =====================
def forgetting_factor(days_passed: int) -> float:
    return exp(-days_passed / 7)

def pressure_mode(days_left: int):
    if days_left > 60:
        return "normal", 1.0
    if days_left > 30:
        return "high-pressure", 1.3
    return "panic", 1.6

def analyze_topics(topics):
    conn = db()
    cur = conn.cursor()
    now = datetime.utcnow()
    analysis = {}

    for topic in topics:
        cur.execute("""
        SELECT score, created_at
        FROM topic_feedback
        WHERE topic = ?
        """, (topic,))
        rows = cur.fetchall()

        if not rows:
            analysis[topic] = {
                "status": "new",
                "confidence": 0.0,
                "priority": 1,
                "last_seen_days": None
            }
            continue

        weighted_sum = 0
        weight_total = 0
        last_seen = None

        for score, created_at in rows:
            ts = datetime.fromisoformat(created_at)
            days_passed = (now - ts).days
            decay = forgetting_factor(days_passed)

            weighted_sum += score * decay
            weight_total += decay

            if not last_seen or ts > last_seen:
                last_seen = ts

        confidence = weighted_sum / weight_total
        days_since_last = (now - last_seen).days

        if confidence < 50 or days_since_last > 10:
            status = "weak"
            priority = 1
        elif confidence < 75 or days_since_last > 5:
            status = "medium"
            priority = 2
        else:
            status = "strong"
            priority = 3

        analysis[topic] = {
            "status": status,
            "confidence": round(confidence, 2),
            "priority": priority,
            "last_seen_days": days_since_last
        }

    conn.close()
    return analysis

# ===================== API =====================
@app.get("/api/v1/health")
def health():
    return {
        "status": "ok",
        "env": ENV
    }

@app.post("/api/v1/generate-plan")
def generate_plan(req: PlanRequest):
    today = date.today()
    days_left = (req.exam_date - today).days

    mode, multiplier = pressure_mode(days_left)
    topic_data = analyze_topics(req.topics)

    sorted_topics = sorted(
        topic_data.items(),
        key=lambda x: x[1]["priority"]
    )

    total_hours = int(req.daily_hours * multiplier)
    hours_left = total_hours
    plan = []

    for topic, data in sorted_topics:
        if hours_left <= 0:
            break

        if data["status"] == "weak":
            hours = min(3 if mode == "panic" else 2, hours_left)
            task = "intensive revision + PYQs"
        elif data["status"] == "medium":
            hours = min(2, hours_left)
            task = "practice + revise"
        else:
            hours = 1
            task = "quick recall"

        hours_left -= hours

        plan.append(
            f"{topic}: {hours}h → {task} "
            f"(confidence {data['confidence']}%)"
        )

    if mode == "panic":
        plan.append("⚠️ DAILY MOCK TEST")
        plan.append("⚠️ ERROR LOG ANALYSIS")

    return {
        "exam": req.exam,
        "days_left": days_left,
        "mode": mode,
        "daily_plan": plan
    }

@app.post("/api/v1/submit-topic-feedback")
def submit_topic_feedback(req: TopicFeedback):
    conn = db()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO topic_feedback (topic, score, completed, time_spent, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (
        req.topic,
        req.score,
        req.completed,
        req.time_spent,
        datetime.utcnow().isoformat()
    ))
    conn.commit()
    conn.close()

    return {
        "message": "Feedback stored",
        "topic": req.topic
    }