from typing import Any

from httpx import AsyncClient, Response
from starlette import status

from tests.mixins import BaseTestCase
from utils.images import generate_test_image


class TestAvatarUpload(BaseTestCase):
    url_name = 'upload_user_avatar'

    async def _request(self, client: AsyncClient, **kwargs: Any) -> Response:
        return await client.post(self.url_path(), **kwargs)

    async def test_user_unauthorized_without_token(self, client: AsyncClient) -> None:
        await self._test_user_unauthorized_without_token(client)

    async def test_unauthorized_with_fake_token(self, client: AsyncClient) -> None:
        await self._test_unauthorized_with_fake_token(client, headers={'Authorization': 'Bearer fake'})

    async def test_user_success(self, client: AsyncClient) -> None:
        token = await self.authorized_user_token()
        response = await self._request(client,
                                       headers={'Authorization': f'Bearer {token}'},
                                       files={'image': ('test.gif', generate_test_image())})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json() == {'detail': 'Unsupported image type'}

    async def test_upload_success(self, client: AsyncClient) -> None:
        token = await self.authorized_user_token()
        response = await self._request(client,
                                       headers={'Authorization': f'Bearer {token}'},
                                       files={'image': ('test.jpg', generate_test_image())})
        assert response.status_code == status.HTTP_200_OK
        assert 'avatar_url' in response.json()
