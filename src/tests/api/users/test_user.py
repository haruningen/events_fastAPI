from typing import Any

from httpx import AsyncClient, Response
from starlette import status

from tests.mixins import BaseTestCase


class TestUsers(BaseTestCase):
    url_name = 'get_user'

    async def _request(self, httpx_client: AsyncClient, **kwargs: Any) -> Response:
        return await httpx_client.get(self.url_path(), **kwargs)

    async def test_user_success(self, httpx_client: AsyncClient) -> None:
        token = await self.authorized_user_token()
        response = await self._request(httpx_client,
                                       headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'email' in data and 'avatar_url' in data

    async def test_user_unauthorized_without_token(self, httpx_client: AsyncClient) -> None:
        await self._test_user_unauthorized_without_token(httpx_client)

    async def test_unauthorized_with_fake_token(self, httpx_client: AsyncClient) -> None:
        await self._test_unauthorized_with_fake_token(httpx_client, headers={'Authorization': 'Bearer fake'})
