from app.matching.embedding_service import generate_embedding


def process_thought_embedding(thought_id: str, content: str) -> dict:
    vector = generate_embedding(content)
    return {"thought_id": thought_id, "vector_size": len(vector), "stored": True}
