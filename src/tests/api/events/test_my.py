from typing import Any

from httpx import AsyncClient, Response
from starlette import status

from tests.mixins import BaseTestCase


class TestEventsMy(BaseTestCase):
    url_name = 'get_user_events'

    async def _request(self, client: AsyncClient, **kwargs: Any) -> Response:
        token = kwargs.pop('token', None)
        return await client.get(
            self.url_path(),
            headers={'Authorization': f'Bearer {token}'} if token else {},
        )

    async def test_events_my_success(self, client: AsyncClient) -> None:
        user, event = await self.attend_event()
        token = await self.authorized_user_token(user)
        response = await self._request(client, token=token)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'items' in data and 'count' in data

    async def test_user_unauthorized_without_token(self, client: AsyncClient) -> None:
        await self._test_user_unauthorized_without_token(client)

    async def test_unauthorized_with_fake_token(self, client: AsyncClient) -> None:
        await self._test_unauthorized_with_fake_token(client)
