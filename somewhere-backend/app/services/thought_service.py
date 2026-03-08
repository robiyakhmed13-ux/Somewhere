from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app.core.anti_spam import suspicious_message
from app.moderation.ai_moderator import moderate_text


class ThoughtService:
    def __init__(self) -> None:
        self._items: list[dict] = []

    def create_thought(self, user_id: str, content: str, emotion_tag: str | None, language_code: str) -> dict:
        is_spam, reason = suspicious_message(content, [x["content"] for x in self._items[-10:]])
        if is_spam:
            raise ValueError(f"SPAM_DETECTED:{reason}")

        moderation = moderate_text(content)
        if not moderation.allowed:
            raise ValueError("CONTENT_BLOCKED")

        now = datetime.now(timezone.utc)
        thought = {
            "id": str(uuid4()),
            "user_id": user_id,
            "content": content,
            "emotion_tag": emotion_tag,
            "language_code": language_code,
            "created_at": now,
            "expires_at": now + timedelta(hours=24),
            "reaction_count": 0,
        }
        self._items.append(thought)
        return thought

    def get_feed(self, limit: int = 20) -> list[dict]:
        now = datetime.now(timezone.utc)
        active = [t for t in self._items if t["expires_at"] > now]
        active.sort(key=lambda x: x["created_at"], reverse=True)
        return active[:limit]


thought_service = ThoughtService()
