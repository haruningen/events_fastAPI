from typing import Any

from httpx import AsyncClient, Response
from starlette import status

from tests.mixins import BaseTestCase


class TestUsersLogin(BaseTestCase):
    url_name = 'login'

    login_data = {
        'email': 'test@test.te',
        'password': 'strongPassword1'
    }

    async def _request(self, client: AsyncClient, **kwargs: Any) -> Response:
        return await client.post(self.url_path(), **kwargs)

    async def test_login_user_success(self, client: AsyncClient) -> None:
        user = await self.auth_user()
        self.login_data['email'] = user.email
        response = await self._request(client, json=self.login_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'access_token' in data and 'refresh_token' in data

    async def test_login_user_tfa_enabled(self, client: AsyncClient) -> None:
        user = await self.auth_user_tfa()
        self.login_data['email'] = user.email
        response = await self._request(client, json=self.login_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'otp_required': True}

    async def test_login_user_not_exit(self, client: AsyncClient) -> None:
        response = await self._request(client, json=self.login_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'User with this email does not exist'}

    async def test_login_user_not_verified(self, client: AsyncClient) -> None:
        user = await self.auth_user(verified=False)
        self.login_data['email'] = user.email
        response = await self._request(client, json=self.login_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Please verify your email address'}

    async def test_login_user_wrong_password(self, client: AsyncClient) -> None:
        user = await self.auth_user()
        self.login_data['email'] = user.email
        self.login_data['password'] = 'strongPassword2'
        response = await self._request(client, json=self.login_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'detail': 'Incorrect Email or Password'}
