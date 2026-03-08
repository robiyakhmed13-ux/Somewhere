from pydantic import BaseModel, Field


class GuestSessionRequest(BaseModel):
    installation_id: str
    platform: str
    app_version: str
    locale: str = "en"
    timezone: str = "UTC"


class RefreshSessionRequest(BaseModel):
    refresh_token: str


class RevokeSessionRequest(BaseModel):
    refresh_token: str


class SessionTokens(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int = Field(description="Access token expiration in seconds")
