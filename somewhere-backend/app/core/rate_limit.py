import time

import redis

from app.config import settings

r = redis.Redis.from_url(settings.redis_url, decode_responses=True)


def check_rate_limit(key: str, limit: int, window_seconds: int) -> tuple[bool, int, int]:
    now = int(time.time())
    bucket = f"{key}:{now // window_seconds}"

    current = r.incr(bucket)
    if current == 1:
        r.expire(bucket, window_seconds)

    allowed = current <= limit
    remaining = max(0, limit - current)
    reset_at = ((now // window_seconds) + 1) * window_seconds
    return allowed, remaining, reset_at
