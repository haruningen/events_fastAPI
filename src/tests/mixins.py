import pytest
from starlette.datastructures import URLPath

from connections.postgresql import Base, async_engine
from gen_typing import YieldAsyncFixture
from main import app


class PostgresMixin:
    """Class for PostgreSQL fixtures"""

    @pytest.fixture(autouse=True)
    async def setup_postgres(self) -> YieldAsyncFixture[None]:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield

        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


class BaseTestCase(PostgresMixin):
    """Base test class"""

    url_name: str

    def url_path(self, **kwargs: int | str) -> URLPath:
        return app.router.url_path_for(self.url_name, **kwargs)
