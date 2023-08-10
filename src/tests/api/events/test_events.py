from typing import Any

from httpx import AsyncClient, Response
from starlette import status

from tests.mixins import BaseTestCase


class TestEvents(BaseTestCase):
    url_name = 'get_events'

    async def _request(self, client: AsyncClient, **kwargs: Any) -> Response:
        return await client.get(self.url_path(), **kwargs)

    async def test_events_success(self, client: AsyncClient) -> None:
        await self.event()
        response = await self._request(client)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'items' in data and 'count' in data
