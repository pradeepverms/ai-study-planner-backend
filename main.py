from datetime import date
from schemas import DailyPlanItem
from utils import expand_topics, compute_mode, confidence_by_mode, split_hours


def generate_plan(
    exam: str,
    exam_date: date,
    daily_hours: int,
    level: str,
    topics: list[str],
):
    today = date.today()
    days_left = (exam_date - today).days

    mode = compute_mode(days_left)
    confidence = confidence_by_mode(mode)

    expanded_topics = expand_topics(topics)
    per_topic_hours = split_hours(daily_hours, len(expanded_topics))

    plan = []

    for subtopic in expanded_topics:
        plan.append(
            DailyPlanItem(
                topic=subtopic.split()[0],
                subtopic=subtopic,
                duration_hours=per_topic_hours,
                activity="revision + PYQs" if mode != "normal" else "concept + recall",
                confidence=confidence,
            )
        )

    return days_left, mode, plan