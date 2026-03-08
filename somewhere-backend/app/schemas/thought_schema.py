from datetime import datetime

from pydantic import BaseModel, Field


class CreateThoughtRequest(BaseModel):
    content: str = Field(min_length=1, max_length=200)
    emotion_tag: str | None = None
    language_code: str = "en"


class ThoughtOut(BaseModel):
    id: str
    content: str
    emotion_tag: str | None
    language_code: str | None
    created_at: datetime
    expires_at: datetime
    reaction_count: int
