from typing import Dict

def analyze_feedback(feedback: Dict) -> Dict:
    accuracy = feedback["accuracy"]
    time_spent = feedback["time_spent"]
    completed = feedback["completed"]

    if not completed:
        return {
            "adjustment": "reduce_load",
            "next_day_hours": max(2, time_spent - 1),
            "reason": "Task not completed. Reducing load to rebuild consistency."
        }

    if accuracy < 50:
        return {
            "adjustment": "increase_practice",
            "next_day_hours": time_spent + 1,
            "reason": "Low accuracy. Increasing practice time."
        }

    if accuracy < 75:
        return {
            "adjustment": "balanced",
            "next_day_hours": time_spent,
            "reason": "Average accuracy. Keeping difficulty stable."
        }

    return {
        "adjustment": "increase_difficulty",
        "next_day_hours": time_spent + 1,
        "reason": "High accuracy. Increasing challenge level."
    }