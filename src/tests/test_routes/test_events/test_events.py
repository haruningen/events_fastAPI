from httpx import AsyncClient
from starlette import status

from tests.mixins import BaseTestCase


class TestEvents(BaseTestCase):
    url_name = 'get_events'

    async def test_events_success(self, httpx_client: AsyncClient) -> None:
        await self.event()
        response = await httpx_client.get(self.url_path())
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'items' in data and 'count' in data