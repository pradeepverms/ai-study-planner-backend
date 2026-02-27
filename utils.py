from datetime import date
from typing import List
import math

TOPIC_MAP = {
    "math": ["calculus", "linear algebra", "probability"],
    "ml": ["supervised", "unsupervised", "evaluation"],
    "ds": ["statistics", "data cleaning", "visualization"],
}


def expand_topics(topics: List[str]) -> List[str]:
    expanded = []
    for t in topics:
        expanded.extend(TOPIC_MAP.get(t.lower(), [t]))
    return expanded


def compute_mode(days_left: int) -> str:
    if days_left <= 30:
        return "war"
    if days_left <= 60:
        return "panic"
    return "normal"


def confidence_by_mode(mode: str) -> float | None:
    if mode == "normal":
        return 80.0
    return None


def split_hours(total_hours: int, count: int) -> float:
    return round(total_hours / count, 2)