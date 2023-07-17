import secrets
from pathlib import Path

from pydantic import HttpUrl
from pydantic_settings import BaseSettings

__all__ = ('Settings',)

DEFAULT_CORS_ORIGINS: list[str] = ['*']


class Settings(BaseSettings):
    # ------- Base settings -------
    BASE_DIR: Path = Path(__file__).parent.parent
    BASE_URL: HttpUrl
    API_ROOT: Path
    ENVIRONMENT: str = 'LOCAL'
    ENV_NAME: str = 'local'
    APP_NAME: str = 'events_fastAPI'
    DEBUG: bool = True
    LOG_LEVEL: str = 'INFO'
    PORT: int = 8080
    SECRET_KEY: str = secrets.token_urlsafe()
    EMAIL_VERIFY_KEY: bytes

    # ---------- Databases ----------

    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str
    POSTGRES_DSN: str

    # ---------- Services ----------

    # SMTP secrets
    EMAIL_HOST_USER: str
    EMAIL_HOST: str
    EMAIL_HOST_PASSWORD: str
    EMAIL_PORT: int
    # Ticketmaster secrets
    TICKETMASTER_API_URL: str
    TICKETMASTER_API_KEY: str
    # Frontend url
    FRONTEND_URL: str
    # Tokens secrets
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str

    class Config:
        env_file = './.env'


settings = Settings()
