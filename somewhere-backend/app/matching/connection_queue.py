import json
import time

import redis

from app.config import settings

r = redis.Redis.from_url(settings.redis_url, decode_responses=True)


class ConnectionQueue:
    def join_queue(self, user_id: str, language_code: str) -> dict:
        queue_key = f"queue:connect:{language_code}"
        dedupe_key = f"queue:member:{language_code}:{user_id}"

        if r.exists(dedupe_key):
            return {"status": "waiting"}

        payload = json.dumps({"user_id": user_id, "joined_at": int(time.time())})
        pipe = r.pipeline()
        pipe.rpush(queue_key, payload)
        pipe.setex(dedupe_key, 600, "1")
        pipe.execute()
        return {"status": "waiting"}

    def leave_queue(self, user_id: str, language_code: str) -> dict:
        queue_key = f"queue:connect:{language_code}"
        dedupe_key = f"queue:member:{language_code}:{user_id}"
        items = r.lrange(queue_key, 0, -1)
        for item in items:
            parsed = json.loads(item)
            if parsed["user_id"] == user_id:
                pipe = r.pipeline()
                pipe.lrem(queue_key, 1, item)
                pipe.delete(dedupe_key)
                pipe.execute()
                return {"status": "left"}
        return {"status": "not_found"}

    def pop_match(self, language_code: str) -> tuple[str, str] | None:
        queue_key = f"queue:connect:{language_code}"

        first = r.lpop(queue_key)
        second = r.lpop(queue_key)
        if not first or not second:
            if first:
                r.lpush(queue_key, first)
            return None

        user_1 = json.loads(first)["user_id"]
        user_2 = json.loads(second)["user_id"]
        r.delete(f"queue:member:{language_code}:{user_1}")
        r.delete(f"queue:member:{language_code}:{user_2}")
        return user_1, user_2
