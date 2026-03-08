from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Thought(Base):
    __tablename__ = "thoughts"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    language_code: Mapped[str | None] = mapped_column(String(10), nullable=True)
    emotion_tag: Mapped[str | None] = mapped_column(String(30), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow() + timedelta(hours=24), nullable=False)
    reaction_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    moderation_state: Mapped[str] = mapped_column(String(20), default="approved", nullable=False)
    similarity_ready: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class ThoughtReaction(Base):
    __tablename__ = "thought_reactions"
    __table_args__ = (UniqueConstraint("thought_id", "user_id", name="unique_reaction"),)

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    thought_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("thoughts.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    reaction_type: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
