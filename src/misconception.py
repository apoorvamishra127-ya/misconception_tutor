def detect_misconception(topic, answer):
    answer = answer.lower()

    if topic == "Overfitting":
        if "too simple" in answer:
            return "Confusing overfitting with underfitting"

        if (
            "poorly" in answer
            and "training" in answer
            and "testing" in answer
        ):
            return "Confusing overfitting with underfitting"

        if "performs poorly on training" in answer:
            return "Confusing overfitting with underfitting"

    if topic == "Underfitting":
        if "memorize" in answer or "noise" in answer:
            return "Confusing underfitting with overfitting"

    return "None"
