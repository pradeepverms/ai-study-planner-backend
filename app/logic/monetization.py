PLANS = {
    "FREE": {
        "daily_ai_calls": 3,
        "daily_questions": 10
    },
    "PRO": {
        "daily_ai_calls": 999,
        "daily_questions": 999
    }
}


def can_use_feature(user_plan, feature, used_today):
    limit = PLANS[user_plan][feature]
    return used_today < limit