import re


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def extract_concepts(text):
    concepts = str(text).split(";")

    return [
        clean_text(concept)
        for concept in concepts
    ]
