from typing import Any

from httpx import AsyncClient, Response
from starlette import status

from tests.mixins import BaseTestCase


class TestEventDetail(BaseTestCase):
    url_name = 'get_event'

    async def _request(self, httpx_client: AsyncClient, **kwargs: Any) -> Response:
        event_id = kwargs.pop('event_id', 1)
        return await httpx_client.get(self.url_path(event_id=event_id), **kwargs)

    async def test_event_detail_success(self, httpx_client: AsyncClient) -> None:
        event = await self.event()
        token = await self.authorized_user_token()
        response = await self._request(httpx_client,
                                       event_id=event.id,
                                       headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert event.id == data['id']

    async def test_event_wrong_id(self, httpx_client: AsyncClient) -> None:
        event = await self.event()
        token = await self.authorized_user_token()
        response = await self._request(httpx_client,
                                       event_id=event.id + 1,
                                       headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data['detail'] == f'Event with ID {event.id + 1} does not exist'

    async def test_user_unauthorized_without_token(self, httpx_client: AsyncClient) -> None:
        await self._test_user_unauthorized_without_token(httpx_client)

    async def test_unauthorized_with_fake_token(self, httpx_client: AsyncClient) -> None:
        await self._test_unauthorized_with_fake_token(httpx_client, headers={'Authorization': 'Bearer fake'})
