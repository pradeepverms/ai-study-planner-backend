from datetime import date, timedelta

def generate_daily_plan(exam_date: date, topics: list[str]):
    today = date.today()
    total_days = (exam_date - today).days

    if total_days <= 0:
        return {"error": "Exam date must be in the future"}

    daily_plan = []
    topic_index = 0

    for i in range(total_days):
        current_date = today + timedelta(days=i)
        topic = topics[topic_index % len(topics)]

        daily_plan.append({
            "date": current_date.isoformat(),
            "topic": topic,
            "tasks": [
                f"Study theory of {topic}",
                f"Solve 10 practice questions from {topic}"
            ]
        })

        topic_index += 1

    return {
        "total_days": total_days,
        "daily_plan": daily_plan
    }