from typing import List
from schemas import DayPlan, DailySlot


def build_daily_plan(topics: List[str], daily_hours: int, day: int) -> DayPlan:
    slots = []
    hours_left = daily_hours

    for topic in topics:
        if hours_left <= 0:
            break
        slots.append(
            DailySlot(
                topic=topic,
                duration="1h",
                type="concept" if day <= 3 else "practice"
            )
        )
        hours_left -= 1

    if hours_left > 0:
        slots.append(
            DailySlot(
                topic="Revision",
                duration=f"{hours_left}h",
                type="recall"
            )
        )

    return DayPlan(
        day=day,
        focus="Learning" if day <= 3 else "Reinforcement",
        schedule=slots
    )


def revision_strategy():
    return {
        "same_day": "Quick recall (30%)",
        "day_3": "Weak areas (70%)",
        "day_7": "Full recall (90%)"
    }