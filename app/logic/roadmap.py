from datetime import date, timedelta

def generate_daily_plan(exam_date: date, topics: list):
    today = date.today()
    days_left = (exam_date - today).days

    if days_left <= 0:
        return {
            "error": "Exam date must be in the future"
        }

    plan = []
    topic_index = 0

    for i in range(days_left):
        current_day = today + timedelta(days=i)
        topic = topics[topic_index % len(topics)]

        plan.append({
            "date": current_day.isoformat(),
            "topic": topic,
            "tasks": [
                f"Read theory of {topic}",
                f"Solve 10 questions from {topic}",
                f"Revise notes of {topic}"
            ]
        })

        topic_index += 1

    return {
        "days_left": days_left,
        "study_plan": plan
    }