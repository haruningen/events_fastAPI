from typing import Any, Optional

import pytest
from httpx import AsyncClient, Response
from starlette import status
from starlette.datastructures import URLPath

from config import settings
from connections.postgresql import Base, async_engine, async_session
from gen_typing import YieldAsyncFixture
from main import app
from models import Event, User
from tests.fixtures.factories import EventFactory, UserFactory, UserTFAFactory
from utils.users import make_token


class PostgresMixin:
    """Class for PostgreSQL fixtures"""

    @pytest.fixture(autouse=True)
    async def setup_postgres(self) -> YieldAsyncFixture[None]:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield

        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


class FactoriesMixin:
    """Class for accessing to factories"""

    @staticmethod
    async def auth_user(**kwargs: str | int | dict) -> User:
        data = UserFactory(**kwargs)
        return await User.create(**data)

    @staticmethod
    async def auth_user_tfa(**kwargs: str | int | dict) -> User:
        data = UserTFAFactory(**kwargs)
        return await User.create(**data)

    @staticmethod
    async def event(**kwargs: str | int | dict) -> Event:
        data = EventFactory(**kwargs)
        return await Event.create(**data)

    async def authorized_user_token(self, user: Optional[User] = None, tfa_enabled: bool = False) -> str:
        if not user:
            if tfa_enabled:
                user = await self.auth_user_tfa()
            else:
                user = await self.auth_user()
        return make_token(
            settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            settings.JWT_SECRET_KEY,
            {'user_id': user.id}
        )

    async def attend_event(self, user: Optional[User] = None, event: Optional[Event] = None) -> tuple[User, Event]:
        if not user:
            user = await self.auth_user()
        if not event:
            event = await self.event()
        await event.add_user(user, async_session())
        return user, event


class BaseTestCase(PostgresMixin, FactoriesMixin):
    """Base test class"""

    url_name: str

    def url_path(self, **kwargs: int | str) -> URLPath:
        return app.router.url_path_for(self.url_name, **kwargs)

    async def _request(self, client: AsyncClient, **kwargs: Any) -> Response:
        raise NotImplementedError()

    async def _test_user_unauthorized_without_token(self, client: AsyncClient) -> None:
        response = await self._request(client)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorized'}

    async def _test_unauthorized_with_fake_token(self, client: AsyncClient, **kwargs: Any) -> None:
        response = await self._request(client, **kwargs)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
