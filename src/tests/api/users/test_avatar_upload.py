from typing import Any

from httpx import AsyncClient, Response
from starlette import status

from tests.mixins import BaseTestCase
from utils.images import generate_test_image


class TestAvatarUpload(BaseTestCase):
    url_name = 'upload_user_avatar'

    async def _request(self, client: AsyncClient, **kwargs: Any) -> Response:
        token = kwargs.pop('token', None)
        image_type = kwargs.pop('image_type', None)
        headers = {'Authorization': f'Bearer {token}'} if token else {}
        return await client.post(
            self.url_path(),
            headers=headers,
            files={'image': (image_type, generate_test_image())}
        )

    async def test_user_unauthorized_without_token(self, client: AsyncClient) -> None:
        await self._test_user_unauthorized_without_token(client)

    async def test_unauthorized_with_fake_token(self, client: AsyncClient) -> None:
        await self._test_unauthorized_with_fake_token(client)

    async def test_unsupported_type(self, client: AsyncClient) -> None:
        token = await self.authorized_user_token()
        response = await self._request(client, token=token, image_type='test.gif')
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json() == {'detail': 'Unsupported image type'}

    async def test_upload_success(self, client: AsyncClient) -> None:
        token = await self.authorized_user_token()
        response = await self._request(client, token=token, image_type='test.jpg')
        assert response.status_code == status.HTTP_200_OK
        assert 'avatar_url' in response.json()
