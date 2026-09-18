from src.pipeline import evaluate_student


def test_correct_overfitting_sample_is_correct():
    result = evaluate_student(
        question="What is overfitting in machine learning?",
        expected_concepts="training performance;test performance;noise",
        student_answer="Overfitting happens when a model learns the training data too closely and performs poorly on new, unseen data.",
        topic="Overfitting",
    )

    assert result["label"] == "Correct"
    assert result["misconception"] == "None"


def test_confusing_underfitting_sample_is_incorrect():
    result = evaluate_student(
        question="What is overfitting in machine learning?",
        expected_concepts="training performance;test performance;noise",
        student_answer="Overfitting occurs when the model performs poorly on both the training data and testing data.",
        topic="Overfitting",
    )

    assert result["label"] == "Incorrect"
    assert result["misconception"] == "Confusing overfitting with underfitting"
