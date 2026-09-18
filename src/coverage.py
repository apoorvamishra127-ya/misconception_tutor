def calculate_coverage(matched, concepts):
    if len(concepts) == 0:
        return 0

    return len(matched) / len(concepts)
