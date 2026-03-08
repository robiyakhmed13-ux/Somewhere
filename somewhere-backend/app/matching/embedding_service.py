
def normalize_text(text: str) -> str:
    return " ".join(text.strip().lower().split())


def generate_embedding(text: str) -> list[float]:
    normalized = normalize_text(text)
    fake_vector = [0.0] * 1536
    fake_vector[0] = len(normalized) / 1000
    return fake_vector
