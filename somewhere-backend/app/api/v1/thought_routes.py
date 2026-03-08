from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.auth import get_current_user_id
from app.core.rate_limit import check_rate_limit
from app.schemas.thought_schema import CreateThoughtRequest
from app.services.thought_service import thought_service

router = APIRouter(prefix="/thoughts", tags=["thoughts"])


@router.post("")
def create_thought(payload: CreateThoughtRequest, user_id: str = Depends(get_current_user_id)) -> dict:
    allowed, _, _ = check_rate_limit(f"thought_create:user:{user_id}", limit=5, window_seconds=600)
    if not allowed:
        raise HTTPException(status_code=429, detail="RATE_LIMIT_EXCEEDED")

    try:
        thought = thought_service.create_thought(
            user_id=user_id,
            content=payload.content,
            emotion_tag=payload.emotion_tag,
            language_code=payload.language_code,
        )
    except ValueError as exc:
        code = str(exc)
        if code.startswith("SPAM_DETECTED"):
            raise HTTPException(status_code=429, detail="RATE_LIMIT_EXCEEDED") from exc
        raise HTTPException(status_code=400, detail=code) from exc

    return {"success": True, "data": {"thought": thought}}


@router.get("/feed")
def get_feed(
    limit: int = Query(default=20, ge=1, le=50),
    _: str = Depends(get_current_user_id),
) -> dict:
    items = thought_service.get_feed(limit=limit)
    return {"success": True, "data": {"items": items, "next_cursor": None}}
