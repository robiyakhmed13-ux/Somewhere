from fastapi import FastAPI

from app.api.v1.connection_routes import router as connection_router
from app.api.v1.session_routes import router as session_router
from app.api.v1.thought_routes import router as thought_router
from app.config import settings
from app.websocket.chat_gateway import router as ws_router

app = FastAPI(title=settings.app_name)

app.include_router(session_router, prefix=settings.api_prefix)
app.include_router(thought_router, prefix=settings.api_prefix)
app.include_router(connection_router, prefix=settings.api_prefix)
app.include_router(ws_router)


@app.get("/health")
def health() -> dict:
    return {"ok": True}
