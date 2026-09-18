def generate_feedback(
    label,
    matched,
    missing,
    misconception
):

    if label == "Correct":

        return (
            "Good job. Your answer covers the "
            "important concepts."
        )

    if label == "Partially Correct":

        if len(matched) == 1:
            matched_text = matched[0]
        elif len(matched) == 2:
            matched_text = matched[0] + " and " + matched[1]
        else:
            matched_text = ", ".join(matched[:-1]) + ", and " + matched[-1]

        missing_text = ", ".join(missing)

        return (
            "Your answer is partially correct. "
            "You correctly explained "
            + matched_text
            + ". You should also explain "
            + missing_text
            + "."
        )

    if misconception == "Confusing overfitting with underfitting":

        return (
            "Overfitting occurs when a model performs very well on training data "
            "but performs poorly on unseen data. Performing poorly on both training "
            "and testing data is associated with underfitting."
        )

    if misconception != "None":

        return (
            "Your answer contains a possible misconception. "
            "Review the difference between the related concepts "
            "and try answering again."
        )

    return (
        "Your answer does not cover the main concepts. "
        "Review the topic and try again."
    )
