from typing import Any

from httpx import AsyncClient, Response
from starlette import status

from tests.mixins import BaseTestCase


class TestUsers(BaseTestCase):
    url_name = 'get_user'

    async def _request(self, client: AsyncClient, **kwargs: Any) -> Response:
        token = kwargs.pop('token', None)
        headers = {'Authorization': f'Bearer {token}'} if token else {}
        return await client.get(
            self.url_path(),
            headers=headers,
        )

    async def test_user_success(self, client: AsyncClient) -> None:
        token = await self.authorized_user_token()
        response = await self._request(client, token=token)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'email' in data and 'avatar_url' in data

    async def test_user_unauthorized_without_token(self, client: AsyncClient) -> None:
        await self._test_user_unauthorized_without_token(client)

    async def test_unauthorized_with_fake_token(self, client: AsyncClient) -> None:
        await self._test_unauthorized_with_fake_token(client)
