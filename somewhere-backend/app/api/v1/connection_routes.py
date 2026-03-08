from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import get_current_user_id
from app.core.rate_limit import check_rate_limit
from app.matching.connection_queue import ConnectionQueue
from app.matching.matchmaker import try_create_match
from app.services.identity_service import IdentityService

router = APIRouter(prefix="/connect", tags=["connect"])
queue = ConnectionQueue()
identity_service = IdentityService()


@router.post("/join-queue")
def join_queue(
    payload: dict,
    user_id: str = Depends(get_current_user_id),
) -> dict:
    allowed, _, _ = check_rate_limit(f"queue_join:user:{user_id}", limit=10, window_seconds=600)
    if not allowed:
        raise HTTPException(status_code=429, detail="RATE_LIMIT_EXCEEDED")

    language_code = payload.get("language_code", "en")
    data = queue.join_queue(user_id=user_id, language_code=language_code)
    maybe_room = try_create_match(language_code)
    if maybe_room:
        socket = identity_service.create_socket_token(user_id, maybe_room["id"])
        return {
            "success": True,
            "data": {
                "status": "matched",
                "room_id": maybe_room["id"],
                "socket_token": socket["socket_token"],
                "expires_at": maybe_room["expires_at"],
            },
        }

    return {
        "success": True,
        "data": {
            "queue_status": data["status"],
            "joined_at": datetime.now(timezone.utc).isoformat(),
            "estimated_wait_seconds": 20,
        },
    }


@router.post("/leave-queue")
def leave_queue(payload: dict, user_id: str = Depends(get_current_user_id)) -> dict:
    language_code = payload.get("language_code", "en")
    result = queue.leave_queue(user_id=user_id, language_code=language_code)
    return {"success": True, "data": {"queue_status": result["status"]}}


@router.get("/status")
def queue_status() -> dict:
    return {"success": True, "data": {"status": "waiting", "estimated_wait_seconds": 12}}
