from pathlib import Path
import pickle

DATASET_PATH = Path(r"D:\aiml_bootcamp_550k_training_samples.csv")
ARTIFACT_PATH = Path(__file__).resolve().parents[1] / "artifacts" / "answer_correctness_model.pkl"


class DatasetClassifier:
    def __init__(self, artifact_path=ARTIFACT_PATH):
        self.artifact_path = Path(artifact_path)
        self.model = None
        self.vectorizer = None
        self.dataset_path = DATASET_PATH
        self.example_count = 0
        self.target = "is_correct"
        self._load()

    @staticmethod
    def _build_text(topic, question, expected_concepts, student_answer):
        return " ".join(
            [
                str(topic or ""),
                str(question or ""),
                str(expected_concepts or ""),
                str(student_answer or ""),
            ]
        )

    def _load(self):
        if not self.artifact_path.exists():
            return
        with self.artifact_path.open("rb") as artifact_file:
            artifact = pickle.load(artifact_file)
        self.model = artifact["model"]
        self.vectorizer = artifact["vectorizer"]
        self.dataset_path = Path(artifact["dataset_path"])
        self.example_count = artifact["example_count"]
        self.target = artifact["target"]

    def predict(self, topic, question, expected_concepts, student_answer):
        if self.model is None or self.vectorizer is None:
            return {"label": None, "confidence": 0.0}
        text = self._build_text(topic, question, expected_concepts, student_answer)
        features = self.vectorizer.transform([text])
        probabilities = self.model.predict_proba(features)[0]
        correct_probability = float(probabilities[1])
        return {
            "label": "Correct" if correct_probability >= 0.5 else "Incorrect",
            "confidence": max(correct_probability, 1 - correct_probability),
            "is_correct_probability": correct_probability,
        }


classifier = DatasetClassifier()


def predict_label(topic, question, expected_concepts, student_answer):
    return classifier.predict(topic, question, expected_concepts, student_answer)


def training_summary():
    return {
        "dataset_path": str(classifier.dataset_path),
        "example_count": classifier.example_count,
        "target": classifier.target,
        "trained": classifier.model is not None,
    }
