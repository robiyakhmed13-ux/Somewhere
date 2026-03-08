from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import get_current_user_id
from app.core.security import decode_token
from app.schemas.session_schema import (
    GuestSessionRequest,
    RefreshSessionRequest,
    RevokeSessionRequest,
)
from app.services.identity_service import IdentityService

router = APIRouter(prefix="/session", tags=["session"])
service = IdentityService()


@router.post("/guest")
def create_guest_session(payload: GuestSessionRequest) -> dict:
    _ = payload
    user_id = str(uuid4())
    tokens = service.create_guest_session(user_id)
    return {
        "success": True,
        "data": {
            "user": {
                "id": user_id,
                "status": "active",
                "locale": payload.locale,
                "timezone": payload.timezone,
            },
            "tokens": tokens,
        },
    }


@router.post("/refresh")
def refresh_session(payload: RefreshSessionRequest) -> dict:
    try:
        parsed = decode_token(payload.refresh_token)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=401, detail="TOKEN_EXPIRED") from exc

    if parsed.get("scope") != "refresh":
        raise HTTPException(status_code=403, detail="FORBIDDEN")

    user_id = parsed["sub"]
    tokens = service.refresh(user_id)
    return {"success": True, "data": tokens}


@router.post("/revoke")
def revoke_session(payload: RevokeSessionRequest, _: str = Depends(get_current_user_id)) -> dict:
    _ = payload
    return {"success": True, "data": {"revoked": True}}
