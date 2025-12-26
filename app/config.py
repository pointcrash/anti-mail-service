from pathlib import Path

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 5
    max_overflow: int = 10


class SMTPConfig(BaseModel):
    host: str = "smtp.example.com"
    port: int = 587
    user: str = "user@example.com"
    password: str = "password"
    from_email: str = "noreply@example.com"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            BASE_DIR / ".env.example",
            BASE_DIR / ".env",
        ),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra='allow',
    )

    db: DatabaseConfig
    smtp: SMTPConfig

    DEBUG: bool = True
    USE_REAL_SMTP: bool = False


settings = Settings()
