import uuid
from datetime import datetime, timedelta, timezone

from app.matching.connection_queue import ConnectionQueue

queue = ConnectionQueue()


def try_create_match(language_code: str) -> dict | None:
    pair = queue.pop_match(language_code)
    if not pair:
        return None

    user_1, user_2 = pair
    return {
        "id": str(uuid.uuid4()),
        "user_1_id": user_1,
        "user_2_id": user_2,
        "status": "waiting_for_join",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "expires_at": (datetime.now(timezone.utc) + timedelta(minutes=6)).isoformat(),
    }
