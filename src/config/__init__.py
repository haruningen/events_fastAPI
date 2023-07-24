from functools import lru_cache
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

from .settings import Settings

__all__ = ('Settings', 'settings', 'oauth')

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

# Set up OAuth
config_data = {'GOOGLE_CLIENT_ID': settings.GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': settings.GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)