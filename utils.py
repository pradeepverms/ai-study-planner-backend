from datetime import date


def days_left(exam_date: date) -> int:
    return (exam_date - date.today()).days


def determine_mode(days: int) -> str:
    if days > 180:
        return "normal"
    elif 60 < days <= 180:
        return "intensive"
    else:
        return "panic"