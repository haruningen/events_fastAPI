import asyncio
from pathlib import Path

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient

from config import settings
from gen_typing import YieldAsyncFixture
from main import app
from refresh_db import create_database
from tests.fixtures.base import *  # noqa: F401,F403

mark_async = pytest.mark.asyncio
POSTGRES_DEFAULT_DB = 'postgres'


@pytest.fixture(scope='session')
def event_loop() -> asyncio.AbstractEventLoop:
    try:
        return asyncio.get_event_loop()
    except RuntimeError as e:
        if 'There is no current event loop in thread' in str(e):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

    return asyncio.get_event_loop()


@pytest.fixture(scope='session', autouse=True)
async def setup(event_loop: asyncio.AbstractEventLoop) -> YieldAsyncFixture[None]:
    """
    Set test environment and media root
    And clear media root in the end
    """

    # Create test database if not exists
    await create_database(str(settings.POSTGRES_DSN))

    yield

    # Remove nested avatars directory with files
    avatars_path: Path = settings.MEDIA_ROOT.joinpath(settings.AVATARS_DIR)
    assert avatars_path and isinstance(avatars_path, Path), 'AVATARS_DIR must be provided'

    if avatars_path.exists():
        for file in avatars_path.glob('*'):
            file.unlink()
        avatars_path.rmdir()

    # Remove media directory with files
    if settings.MEDIA_ROOT.exists():
        for file in settings.MEDIA_ROOT.glob('*'):
            file.unlink()
        settings.MEDIA_ROOT.rmdir()


@pytest.fixture
async def test_app() -> YieldAsyncFixture[FastAPI]:
    """Handle app's lifespan events"""

    async with LifespanManager(app):
        yield app


@pytest.fixture
async def httpx_client(test_app: FastAPI) -> YieldAsyncFixture[AsyncClient]:
    """Init httpx client"""

    async with AsyncClient(app=test_app, base_url=f'http://0.0.0.0:{settings.PORT}') as client:
        yield client
