import secrets
from pathlib import Path

from bcrypt import gensalt
from pydantic import FieldValidationInfo, HttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ('Settings',)

DEFAULT_CORS_ORIGINS: list[str] = ['*']


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='./.env')

    # ------- Base settings -------
    BASE_DIR: Path = Path(__file__).parent.parent
    BASE_URL: HttpUrl
    API_ROOT: Path
    ENVIRONMENT: str = 'LOCAL'
    APP_NAME: str = 'events_fastAPI'
    DEBUG: bool = True
    LOG_LEVEL: str = 'INFO'
    PORT: int = 8080
    SECRET_KEY: str = secrets.token_urlsafe()
    EMAIL_VERIFY_KEY: bytes
    RESET_PASSWORD_KEY: bytes
    PASSWORD_SALT: bytes = gensalt()
    DATA_HANDLER_TOTAL_PAGE: int = 3
    DATA_HANDLER_PER_PAGE: int = 10

    # ---------- Storage ----------

    MEDIA_ROOT: Path = Path('media')
    MEDIA_URL: HttpUrl
    AVATARS_DIR: Path = Path('avatars')

    # ---------- Databases ----------

    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str
    POSTGRES_DSN: str

    # ---------- Celery ----------

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    # ---------- Services ----------

    # SMTP secrets
    EMAIL_HOST_USER: str
    EMAIL_HOST: str
    EMAIL_HOST_PASSWORD: str
    EMAIL_PORT: int
    # Frontend url
    FRONTEND_URL: str
    # Tokens secrets
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    # Google secrets
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    OAUTH_SESSION_KEY: str
    GOOGLE_OAUTH_URL: str = 'https://accounts.google.com/.well-known/openid-configuration'

    # ---------- Non env settings ----------

    IMAGE_EXTENSIONS: tuple[str, ...] = ('.jpg', '.png', '.jpeg')

    # ---------- Validators ----------

    @field_validator('MEDIA_ROOT')
    def create_media_root_dir(cls, v: Path, info: FieldValidationInfo) -> Path:
        base_dir = info.data.get('BASE_DIR')
        assert base_dir and isinstance(base_dir, Path), 'BASE_DIR must be provided'

        media_root = base_dir.joinpath(v)
        media_root.mkdir(parents=True, exist_ok=True)
        return media_root

    @field_validator('AVATARS_DIR')
    def create_avatars_dir(cls, v: Path, info: FieldValidationInfo) -> Path:
        media_root = info.data.get('MEDIA_ROOT')
        assert media_root and isinstance(media_root, Path), 'MEDIA_ROOT must be provided'

        media_root.joinpath(v).mkdir(parents=True, exist_ok=True)
        return v
