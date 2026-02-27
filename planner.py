from datetime import date
from typing import List
from schemas import PlanRequest, PlanResponse, TopicPlan, SubTopicPlan


# STATIC KNOWLEDGE GRAPH (INTENTIONAL)
TOPIC_GRAPH = {
    "calculus": {
        "limits": 1,
        "continuity": 1,
        "differentiation": 2,
        "applications_of_derivatives": 2
    }
}


def calculate_days_left(exam_date: str) -> int:
    exam = date.fromisoformat(exam_date)
    today = date.today()
    return max((exam - today).days, 0)


def decide_mode(days_left: int) -> str:
    if days_left < 60:
        return "panic"
    if days_left < 180:
        return "revision"
    return "normal"


def generate_plan(req: PlanRequest) -> PlanResponse:
    days_left = calculate_days_left(req.exam_date)
    mode = decide_mode(days_left)

    daily_plan: List[TopicPlan] = []

    for topic in req.topics:
        topic_key = topic.lower()

        if topic_key not in TOPIC_GRAPH:
            continue  # unknown topic ignored (by design)

        subtopics = TOPIC_GRAPH[topic_key]
        total_weight = sum(subtopics.values())
        total_minutes = req.daily_hours * 60

        subtopic_plans: List[SubTopicPlan] = []

        for name, weight in subtopics.items():
            minutes = int((weight / total_weight) * total_minutes)

            if weight == 1:
                activity = "concept building + solved examples"
                confidence = 0.55
            else:
                activity = "problem solving + PYQs"
                confidence = 0.35

            if mode == "revision":
                activity = "revision + PYQs"
                confidence += 0.15

            if mode == "panic":
                activity = "rapid revision + error fixing"
                confidence -= 0.10

            subtopic_plans.append(
                SubTopicPlan(
                    name=name,
                    duration_minutes=minutes,
                    activity=activity,
                    confidence=round(max(min(confidence, 0.95), 0.1), 2)
                )
            )

        daily_plan.append(
            TopicPlan(
                topic=topic_key,
                total_hours=req.daily_hours,
                subtopics=subtopic_plans
            )
        )

    return PlanResponse(
        exam=req.exam,
        days_left=days_left,
        mode=mode,
        daily_plan=daily_plan
    )