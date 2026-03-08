from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

from app.core.security import decode_token
from app.moderation.ai_moderator import moderate_text
from app.websocket.manager import manager

router = APIRouter()


@router.websocket("/ws/chat/{room_id}")
async def websocket_chat(websocket: WebSocket, room_id: str, token: str = Query(...)) -> None:
    try:
        payload = decode_token(token)
        if payload.get("scope") != "socket":
            await websocket.close(code=1008)
            return
    except Exception:  # noqa: BLE001
        await websocket.close(code=1008)
        return

    await manager.connect(room_id, websocket)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)

    await manager.broadcast(
        room_id,
        {
            "event": "room.started",
            "data": {
                "room_id": room_id,
                "started_at": datetime.now(timezone.utc).isoformat(),
                "expires_at": expires_at.isoformat(),
            },
        },
    )

    try:
        while True:
            if datetime.now(timezone.utc) >= expires_at:
                await manager.broadcast(
                    room_id,
                    {
                        "event": "room.expired",
                        "data": {"room_id": room_id, "ended_at": datetime.now(timezone.utc).isoformat()},
                    },
                )
                break

            payload = await websocket.receive_json()
            event = payload.get("event")
            data = payload.get("data", {})

            if event == "chat.send_message":
                content = str(data.get("content", ""))
                moderation = moderate_text(content)
                if not moderation.allowed:
                    await websocket.send_json(
                        {
                            "event": "chat.message_blocked",
                            "data": {
                                "client_message_id": data.get("client_message_id"),
                                "reason_code": "CONTENT_BLOCKED",
                            },
                        }
                    )
                    continue

                await manager.broadcast(
                    room_id,
                    {
                        "event": "chat.message",
                        "data": {
                            "room_id": room_id,
                            "content": content,
                            "message_type": data.get("message_type", "text"),
                            "created_at": datetime.now(timezone.utc).isoformat(),
                        },
                    },
                )
            elif event == "chat.typing":
                await manager.broadcast(
                    room_id,
                    {
                        "event": "chat.typing",
                        "data": {
                            "room_id": room_id,
                            "is_typing": bool(data.get("is_typing", False)),
                        },
                    },
                )
            elif event == "chat.leave_room":
                break

    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(room_id, websocket)
        await manager.broadcast(room_id, {"event": "room.peer_left", "data": {"room_id": room_id}})
