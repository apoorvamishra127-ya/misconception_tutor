from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.preprocess import clean_text


ALIASES = {
    "training performance": {
        "training", "train", "fit", "fitted", "learned", "accuracy",
        "performance", "well", "memorize", "memorized", "overfit"
    },
    "test performance": {
        "test", "testing", "unseen", "new", "generalize", "generalisation",
        "evaluation", "validation", "accuracy", "performance", "poorly", "data"
    },
    "noise": {"noise", "noisy", "random", "memorize", "memorized", "captures"},
}


def _overlap_score(student_answer, concept):
    answer_tokens = set(clean_text(student_answer).split())
    concept_tokens = set(clean_text(concept).split())
    expanded_concept_tokens = set(concept_tokens)
    expanded_concept_tokens |= ALIASES.get(concept, set())

    if not expanded_concept_tokens:
        return 0.0

    overlap = len(answer_tokens & expanded_concept_tokens)
    return overlap / len(expanded_concept_tokens)


def _semantic_match_score(student_answer, concept):
    answer = clean_text(student_answer)
    answer_tokens = set(answer.split())
    concept_text = clean_text(concept)

    if concept_text == "training performance":
        training_signal = any(token in answer_tokens for token in {"training", "train", "fit", "fitted", "learned"})
        quality_signal = any(token in answer_tokens for token in {"performance", "accuracy", "well", "good"})
        if training_signal and quality_signal:
            return 1.0

    if concept_text == "test performance":
        unseen_signal = any(token in answer_tokens for token in {"test", "testing", "unseen", "new", "generalize", "validation", "evaluation"})
        performance_signal = any(token in answer_tokens for token in {"performance", "accuracy", "poorly", "generalize", "data"})
        if unseen_signal and performance_signal:
            return 1.0

    if concept_text == "noise":
        if any(token in answer_tokens for token in {"noise", "noisy", "random", "memorize", "memorized"}):
            return 1.0

    return _overlap_score(answer, concept_text)


def compare_answer(student_answer, concepts):
    texts = [student_answer] + concepts

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(texts)

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:]
    )[0]

    adjusted = []
    for concept, score in zip(concepts, similarity):
        semantic_score = _semantic_match_score(student_answer, concept)
        adjusted.append(max(float(score), float(semantic_score)))

    return adjusted
