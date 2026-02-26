def generate_explanation(question, correct_answer, user_answer, topic):
    if user_answer == correct_answer:
        return {
            "type": "reinforcement",
            "message": f"Correct! Your understanding of {topic} is solid. Keep practicing similar questions."
        }

    return {
        "type": "correction",
        "message": (
            f"You answered '{user_answer}', but the correct answer is '{correct_answer}'.\n\n"
            f"Focus on revising the core concept of {topic}. "
            f"Re-derive the formula and solve 5 similar problems before moving ahead."
        )
    }