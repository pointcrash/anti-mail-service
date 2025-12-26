from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/dbname"
    
    # SMTP Settings (Defaults to mock if not provided)
    SMTP_HOST: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "user@example.com"
    SMTP_PASSWORD: str = "password"
    SMTP_FROM_EMAIL: str = "noreply@example.com"
    
    # If True, valid SMTP credentials are required. If False, sends are simulated.
    USE_REAL_SMTP: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
