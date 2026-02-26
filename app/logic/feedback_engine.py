def evaluate_exam(submissions):
    total = len(submissions)
    score = 0
    topic_stats = {}

    detailed_feedback = []

    for item in submissions:
        topic = item["topic"]
        correct = item["correct_answer"]
        user = item["user_answer"]

        if topic not in topic_stats:
            topic_stats[topic] = {"correct": 0, "total": 0}

        topic_stats[topic]["total"] += 1

        if user == correct:
            score += 1
            topic_stats[topic]["correct"] += 1
            detailed_feedback.append({
                "question_id": item["question_id"],
                "status": "Correct"
            })
        else:
            detailed_feedback.append({
                "question_id": item["question_id"],
                "status": "Wrong",
                "correct_answer": correct
            })

    weak_topics = [
        topic for topic, stat in topic_stats.items()
        if stat["correct"] / stat["total"] < 0.6
    ]

    return {
        "score": score,
        "total": total,
        "percentage": round((score / total) * 100, 2),
        "weak_topics": weak_topics,
        "feedback": detailed_feedback
    }