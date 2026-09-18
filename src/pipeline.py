from src.preprocess import clean_text, extract_concepts
from src.concept_match import find_concepts
from src.coverage import calculate_coverage
from src.classification import classify_answer
from src.misconception import detect_misconception
from src.feedback import generate_feedback
from src.trained_classifier import predict_label, training_summary


def evaluate_student(
    question,
    expected_concepts,
    student_answer,
    topic
):

    # 1. Clean answer
    student_answer = clean_text(student_answer)

    # 2. Get concepts
    concepts = extract_concepts(
        expected_concepts
    )

    # 3. Find matched/missing concepts
    matched, missing = find_concepts(
        student_answer,
        concepts
    )

    # 4. Calculate coverage
    coverage = calculate_coverage(
        matched,
        concepts
    )

    # 5. Classification
    label = classify_answer(
        student_answer,
        matched,
        missing
    )

    learned_result = predict_label(
        topic,
        question,
        expected_concepts,
        student_answer,
    )

    # 6. Misconception
    misconception = detect_misconception(
        topic,
        student_answer
    )

    # 7. Feedback
    feedback = generate_feedback(
        label,
        matched,
        missing,
        misconception
    )

    return {
        "matched": matched,
        "missing": missing,
        "coverage": coverage,
        "label": label,
        "model_prediction": learned_result["label"],
        "model_confidence": learned_result["confidence"],
        "training": training_summary(),
        "misconception": misconception,
        "feedback": feedback
    }
