# Somewhere Backend

Modular-monolith FastAPI backend scaffold for the anonymous-first emotional support platform "Somewhere".

## Implemented foundations

- Anonymous guest session and token flow stubs
- Thought creation and feed retrieval stubs
- Redis-backed connection queue + matchmaker
- WebSocket chat gateway + in-memory room connection manager
- Safety primitives: rule moderation, anti-spam, rate limiting
- Embedding + similarity stubs for pgvector integration

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Notes

This is a startup-ready scaffold, not production-complete. Replace placeholder implementations for:

- token signing/verification and secure hashing policy
- durable DB repositories and migrations
- AI moderation provider integration
- Redis pub/sub and distributed WebSocket fan-out
- embedding provider + pgvector-adapted SQLAlchemy bindings
