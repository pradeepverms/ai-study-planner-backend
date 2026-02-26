def evaluate_answers(user_answers, correct_answers):
    score = 0
    feedback = []

    for i, correct in enumerate(correct_answers):
        if user_answers[i] == correct:
            score += 1
            feedback.append("Correct")
        else:
            feedback.append(f"Wrong (Correct: {correct})")

    return {
        "score": score,
        "total": len(correct_answers),
        "feedback": feedback
    }