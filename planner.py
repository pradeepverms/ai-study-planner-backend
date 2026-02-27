from schemas import PlanRequest, PlanResponse, DailyPlan, Activity
from utils import (
    days_left,
    panic_mode,
    forgetting_curve,
    confidence_score,
    split_subtopics,
    activity_type
)


def generate_plan(payload: PlanRequest) -> PlanResponse:
    remaining_days = days_left(payload.exam_date)
    mode = panic_mode(remaining_days)

    daily_plans = []

    for day in range(1, min(remaining_days, 30) + 1):
        decay = forgetting_curve(day)
        activities = []

        per_topic_hours = payload.daily_hours / len(payload.topics)

        for topic in payload.topics:
            subtopics = split_subtopics(topic)
            subtopic = subtopics[(day - 1) % len(subtopics)]

            confidence = confidence_score(payload.level, decay)

            activities.append(
                Activity(
                    topic=topic,
                    subtopic=subtopic,
                    duration_hours=round(per_topic_hours, 2),
                    activity=activity_type(day, mode),
                    confidence=confidence
                )
            )

        daily_plans.append(
            DailyPlan(
                day=day,
                total_hours=payload.daily_hours,
                activities=activities
            )
        )

    return PlanResponse(
        exam=payload.exam,
        days_left=remaining_days,
        mode=mode,
        daily_plan=daily_plans
    )