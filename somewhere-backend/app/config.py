from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Somewhere API"
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite+pysqlite:///./somewhere.db"
    redis_url: str = "redis://localhost:6379/0"
    access_token_ttl_seconds: int = 1800
    refresh_token_ttl_seconds: int = 60 * 60 * 24 * 30
    socket_token_ttl_seconds: int = 300
    secret_key: str = "dev-secret-change-me"
    algorithm: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
