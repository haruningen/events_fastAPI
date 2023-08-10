from fastapi import status
from httpx import AsyncClient as Httpx

from .conftest import mark_async
from .mixins import BaseTestCase


class TestLive(BaseTestCase):
    url_name = 'live'

    @mark_async
    async def test_live(self, client: Httpx) -> None:
        """Test live endpoint"""

        r = await client.get(self.url_path())
        assert r.json() == {'live': 'ok'}
        assert r.status_code == status.HTTP_200_OK
