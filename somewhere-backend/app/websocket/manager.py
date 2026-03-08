from collections import defaultdict

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.room_connections: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(self, room_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.room_connections[room_id].append(websocket)

    def disconnect(self, room_id: str, websocket: WebSocket) -> None:
        if room_id in self.room_connections:
            self.room_connections[room_id] = [ws for ws in self.room_connections[room_id] if ws != websocket]
            if not self.room_connections[room_id]:
                del self.room_connections[room_id]

    async def broadcast(self, room_id: str, message: dict) -> None:
        for ws in self.room_connections.get(room_id, []):
            await ws.send_json(message)


manager = ConnectionManager()
