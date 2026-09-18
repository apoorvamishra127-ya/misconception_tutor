from src.preprocess import clean_text
from src.similarity import compare_answer

THRESHOLD = 0.20


def find_concepts(student_answer, concepts):
    cleaned_answer = clean_text(student_answer)
    cleaned_concepts = [clean_text(concept) for concept in concepts]

    scores = compare_answer(
        cleaned_answer,
        cleaned_concepts
    )

    matched = []
    missing = []

    for concept, score in zip(cleaned_concepts, scores):
        if score >= THRESHOLD:
            matched.append(concept)
        else:
            missing.append(concept)

    return matched, missing
