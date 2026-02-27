from datetime import datetime
from dateutil.parser import parse
import math
import random


def days_left(exam_date: str) -> int:
    today = datetime.utcnow().date()
    exam = parse(exam_date).date()
    return max((exam - today).days, 0)


def panic_mode(days_left: int) -> str:
    if days_left <= 30:
        return "panic"
    if days_left <= 90:
        return "pressure"
    return "normal"


def forgetting_curve(day: int) -> float:
    # Ebbinghaus-inspired decay
    return round(max(0.3, math.exp(-day / 14)), 2)


def confidence_score(level: str, decay: float) -> float:
    base = {
        "beginner": 0.4,
        "intermediate": 0.6,
        "advanced": 0.8
    }.get(level, 0.5)

    return round(min(1.0, base + (1 - decay) * 0.5), 2)


def split_subtopics(topic: str):
    return [
        f"{topic} fundamentals",
        f"{topic} core concepts",
        f"{topic} problem solving",
        f"{topic} PYQs",
        f"{topic} revision"
    ]


def activity_type(day: int, mode: str):
    if mode == "panic":
        return "rapid revision + PYQs"
    if day % 7 == 0:
        return "revision + mock"
    return "concept learning + practice"