from typing import Optional

import pytest
from starlette.datastructures import URLPath

from config import settings
from connections.postgresql import Base, async_engine
from tests.fixtures.factories import UserFactory
from gen_typing import YieldAsyncFixture
from main import app
from models import User
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

    async def authorized_user_token(self, user: Optional[User] = None) -> str:
        if not user:
            user = await self.auth_user()
        return make_token(
            settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            settings.JWT_SECRET_KEY,
            {'user_id': user.id}
        )


class BaseTestCase(PostgresMixin, FactoriesMixin):
    """Base test class"""

    url_name: str

    def url_path(self, **kwargs: int | str) -> URLPath:
        return app.router.url_path_for(self.url_name, **kwargs)
