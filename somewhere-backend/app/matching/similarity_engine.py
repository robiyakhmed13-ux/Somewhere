from sqlalchemy import text
from sqlalchemy.orm import Session


def find_similar_thoughts(db: Session, embedding: list[float], limit: int = 5) -> list[str]:
    query = text(
        """
        SELECT te.thought_id
        FROM thought_embeddings te
        ORDER BY te.embedding <-> :embedding
        LIMIT :limit
        """
    )
    result = db.execute(query, {"embedding": embedding, "limit": limit})
    return [row[0] for row in result.fetchall()]
