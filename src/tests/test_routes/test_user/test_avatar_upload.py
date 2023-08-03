from httpx import AsyncClient
from starlette import status

from tests.mixins import BaseTestCase
from utils.images import generate_test_image


class TestAvatarUpload(BaseTestCase):
    url_name = 'upload_user_avatar'

    async def test_user_unauthorized_without_token(self, httpx_client: AsyncClient) -> None:
        response = await httpx_client.post(self.url_path())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorized'}

    async def test_unauthorized_with_fake_token(self, httpx_client: AsyncClient) -> None:
        response = await httpx_client.post(self.url_path(), headers={'Authorization': 'Bearer fake'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}

    async def test_user_success(self, httpx_client: AsyncClient) -> None:
        token = await self.authorized_user_token()
        response = await httpx_client.post(
            self.url_path(),
            headers={'Authorization': f'Bearer {token}'},
            files={'image': ('test.gif', generate_test_image())}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json() == {'detail': 'Unsupported image type'}

    async def test_upload_success(self, httpx_client: AsyncClient) -> None:
        token = await self.authorized_user_token()
        response = await httpx_client.post(
            self.url_path(),
            headers={'Authorization': f'Bearer {token}'},
            files={'image': ('test.jpg', generate_test_image())}
        )
        assert response.status_code == status.HTTP_200_OK
        assert 'avatar_url' in response.json()
