from pathlib import Path
import pickle

import pandas as pd
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDClassifier

DATASET_PATH = Path(r"D:\aiml_bootcamp_550k_training_samples.csv")
ARTIFACT_PATH = Path(__file__).resolve().parents[1] / "artifacts" / "answer_correctness_model.pkl"
CHUNK_SIZE = 50_000


def build_training_text(frame):
    return (
        frame["question"].fillna("").astype(str)
        + " concept "
        + frame["concept"].fillna("").astype(str)
        + " student answer "
        + frame["student_answer"].fillna("").astype(str)
    )


def train():
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATASET_PATH}")

    columns = [
        "question",
        "student_answer",
        "is_correct",
        "concept",
    ]
    vectorizer = HashingVectorizer(
        lowercase=True,
        n_features=2**18,
        ngram_range=(1, 2),
        alternate_sign=False,
        norm="l2",
    )
    classifier = SGDClassifier(
        loss="log_loss",
        random_state=42,
        average=True,
    )
    classes = [0, 1]
    row_count = 0

    for chunk in pd.read_csv(DATASET_PATH, usecols=columns, chunksize=CHUNK_SIZE):
        chunk = chunk.dropna(subset=["is_correct"])
        if chunk.empty:
            continue
        features = vectorizer.transform(build_training_text(chunk))
        targets = chunk["is_correct"].astype(int).to_numpy()
        classifier.partial_fit(features, targets, classes=classes)
        row_count += len(chunk)
        print(f"trained rows: {row_count}")

    ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with ARTIFACT_PATH.open("wb") as artifact_file:
        pickle.dump(
            {
                "model": classifier,
                "vectorizer": vectorizer,
                "dataset_path": str(DATASET_PATH),
                "example_count": row_count,
                "target": "is_correct",
            },
            artifact_file,
        )
    print(f"saved model: {ARTIFACT_PATH}")
    print(f"training examples: {row_count}")


if __name__ == "__main__":
    train()
