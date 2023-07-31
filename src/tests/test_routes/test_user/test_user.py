from httpx import AsyncClient
from starlette import status

from tests.mixins import BaseTestCase

class TestUsers(BaseTestCase):
    url_name = 'get_user'

    async def test_user_success(self, httpx_client: AsyncClient) -> None:
        token = await self.authorized_user_token()
        response = await httpx_client.get(self.url_path(), headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'email' in data and 'avatar_url' in data

    async def test_user_unauthorized_without_token(self, httpx_client: AsyncClient) -> None:
        response = await httpx_client.get(self.url_path())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorized'}

    async def test_unauthorized_with_fake_token(self, httpx_client: AsyncClient) -> None:
        response = await httpx_client.get(self.url_path(), headers={'Authorization': 'Bearer fake'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
