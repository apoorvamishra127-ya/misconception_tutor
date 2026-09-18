from pathlib import Path
import json

METADATA_PATH = Path(__file__).resolve().parents[1] / "artifacts" / "dataset_metadata.json"

DEFAULT_TOPICS = {
    "Overfitting": "training performance;test performance;noise",
    "Underfitting": "training performance;test performance;model complexity",
    "Bias-Variance": "bias;variance;generalization;training error;test error",
    "Generalization": "training data;unseen data;test performance;noise",
}


def load_metadata():
    if not METADATA_PATH.exists():
        return {}
    with METADATA_PATH.open("r", encoding="utf-8") as metadata_file:
        return json.load(metadata_file).get("topics", {})


DATASET_TOPICS = load_metadata()
TOPIC_OPTIONS = list(dict.fromkeys([*DEFAULT_TOPICS.keys(), *DATASET_TOPICS.keys()]))


def get_expected_concepts(topic):
    return DEFAULT_TOPICS.get(topic, topic)


def get_samples(topic):
    return DATASET_TOPICS.get(topic, [])
