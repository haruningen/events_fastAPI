from functools import lru_cache

from .settings import Settings

__all__ = ('Settings', 'settings',)

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
