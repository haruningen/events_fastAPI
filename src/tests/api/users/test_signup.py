from typing import Any

from httpx import AsyncClient, Response
from starlette import status

from tests.mixins import BaseTestCase


class TestUsersSignUp(BaseTestCase):
    url_name = 'create_user'

    create_data = {
        'email': 'test@test.te',
        'password': 'strongPassword1',
        'password_confirm': 'strongPassword1'
    }

    async def _request(self, client: AsyncClient, **kwargs: Any) -> Response:
        return await client.post(self.url_path(), **kwargs)

    async def test_create_user_success(self, client: AsyncClient) -> None:
        response = await self._request(client, json=self.create_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['email'] == self.create_data['email']
        assert data['avatar_url'] is None

    async def test_create_user_exist(self, client: AsyncClient) -> None:
        user = await self.auth_user()
        self.create_data['email'] = user.email
        response = await self._request(client, json=self.create_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'detail': 'User with this email already exist'}

    async def test_create_user_passwords_dont_match(self, client: AsyncClient) -> None:
        self.create_data['password_confirm'] = 'strongPassword2'
        response = await self._request(client, json=self.create_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json()['detail'][0]['msg'] == 'Value error, Passwords do not match'
