from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_token

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    if not credentials:
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")

    try:
        payload = decode_token(credentials.credentials)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=401, detail="TOKEN_EXPIRED") from exc

    if payload.get("scope") != "access":
        raise HTTPException(status_code=403, detail="FORBIDDEN")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")

    return user_id
