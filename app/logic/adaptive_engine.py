from datetime import date, timedelta


def generate_adaptive_plan(exam_date, topics, weak_topics):
    today = date.today()
    days_left = (exam_date - today).days

    if days_left <= 0:
        return {"error": "Exam date must be in the future"}

    plan = []
    current_day = today

    # Weighting logic
    weighted_topics = []

    for topic in topics:
        if topic in weak_topics:
            weighted_topics.extend([topic] * 3)  # higher priority
        else:
            weighted_topics.append(topic)

    index = 0
    while current_day <= exam_date:
        plan.append({
            "date": current_day.isoformat(),
            "topic": weighted_topics[index % len(weighted_topics)],
            "task": "Study + Practice Questions"
        })
        current_day += timedelta(days=1)
        index += 1

    return {
        "days_left": days_left,
        "adaptive_plan": plan
    }