from pathlib import Path
import json

import pandas as pd

DATASET_PATH = Path(r"D:\aiml_bootcamp_550k_training_samples.csv")
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "artifacts" / "dataset_metadata.json"


def build_metadata():
    columns = ["question", "student_answer", "concept", "is_correct"]
    topics = {}

    for chunk in pd.read_csv(DATASET_PATH, usecols=columns, chunksize=50_000):
        chunk = chunk.dropna(subset=["concept", "question", "student_answer"])
        for concept, concept_rows in chunk.groupby("concept"):
            bucket = topics.setdefault(str(concept), [])
            for _, row in concept_rows.iterrows():
                if len(bucket) >= 5:
                    break
                sample = {
                    "question": str(row["question"]),
                    "answer": str(row["student_answer"]),
                    "is_correct": bool(int(row["is_correct"])),
                }
                if sample not in bucket:
                    bucket.append(sample)

    metadata = {
        "dataset_path": str(DATASET_PATH),
        "topics": topics,
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"saved metadata: {OUTPUT_PATH}")
    print(f"topics: {len(topics)}")


if __name__ == "__main__":
    build_metadata()
