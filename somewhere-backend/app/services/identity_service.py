from app.config import settings
from app.core.security import create_token


class IdentityService:
    def create_guest_session(self, user_id: str) -> dict:
        access_token = create_token(user_id, settings.access_token_ttl_seconds, "access")
        refresh_token = create_token(user_id, settings.refresh_token_ttl_seconds, "refresh")
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": settings.access_token_ttl_seconds,
        }

    def refresh(self, user_id: str) -> dict:
        return self.create_guest_session(user_id)

    def create_socket_token(self, user_id: str, room_id: str) -> dict:
        token = create_token(f"{user_id}:{room_id}", settings.socket_token_ttl_seconds, "socket")
        return {"socket_token": token, "expires_in": settings.socket_token_ttl_seconds}
