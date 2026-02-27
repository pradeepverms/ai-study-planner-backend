from datetime import date
from schemas import DailyPlanItem
from utils import expand_topics, compute_mode, confidence_by_mode, split_hours


def generate_plan(exam, exam_date, daily_hours, level, topics):
    today = date.today()
    days_left = (exam_date - today).days
    mode = compute_mode(days_left)
    confidence = confidence_by_mode(mode)

    expanded_topics = expand_topics(topics)
    hours_per_topic = split_hours(daily_hours, len(expanded_topics))

    daily_plan = []

    for subtopic in expanded_topics:
        daily_plan.append(
            DailyPlanItem(
                topic=topics[0],
                subtopic=subtopic,
                duration_hours=hours_per_topic,
                activity="concept + recall" if mode == "normal" else "revision + PYQs",
                confidence=confidence,
            )
        )

    return days_left, mode, daily_plan