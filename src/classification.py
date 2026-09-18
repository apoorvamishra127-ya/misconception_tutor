def classify_answer(student_answer, matched_concepts, missing_concepts):
    answer = student_answer.lower()

    # Detect contradiction / wrong definition
    if (
        "poorly" in answer
        and "training" in answer
        and "testing" in answer
    ):
        return "Incorrect"

    if "performs poorly on training" in answer:
        return "Incorrect"

    if "too simple" in answer or "cannot learn" in answer:
        return "Incorrect"

    # Strong correct explanations should count even if the optional noise concept is missing.
    has_training_signal = "training" in answer or "train" in answer or "fit" in answer
    has_unseen_signal = "test" in answer or "testing" in answer or "unseen" in answer or "new" in answer or "generalize" in answer
    has_good_train_bad_test = (
        ("training" in answer or "train" in answer)
        and ("unseen" in answer or "test" in answer or "testing" in answer or "new" in answer)
        and ("poor" in answer or "worse" in answer or "not" in answer)
    )

    total = len(matched_concepts) + len(missing_concepts)

    if total == 0:
        return "Incorrect"

    coverage = len(matched_concepts) / total

    if (
        has_training_signal and has_unseen_signal and ("too closely" in answer or "memor" in answer or "poor" in answer)
    ) or has_good_train_bad_test:
        return "Correct"

    if coverage >= 0.75:
        return "Correct"
    elif coverage >= 0.40:
        return "Partially Correct"
    else:
        return "Incorrect"
