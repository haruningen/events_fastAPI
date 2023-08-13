from typing import Any

from httpx import AsyncClient, Response
from starlette import status

from models import User
from tests.fixtures.factories import UserLoginFactory
from tests.mixins import BaseTestCase
from utils.users import make_hashed_password


class TestUsersLogin(BaseTestCase):
    url_name = 'login'

    async def _request(self, client: AsyncClient, **kwargs: Any) -> Response:
        return await client.post(self.url_path(), **kwargs)

    async def test_login_user_success(self, client: AsyncClient) -> None:
        user = UserLoginFactory()
        await User.create(
            email=user['email'],
            hashed_password=make_hashed_password(user['password']),
            verified=True
        )
        response = await self._request(client, json=user)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'access_token' in data and 'refresh_token' in data

    async def test_login_user_tfa_enabled(self, client: AsyncClient) -> None:
        user = UserLoginFactory()
        await User.create(
            email=user['email'],
            hashed_password=make_hashed_password(user['password']),
            verified=True,
            tfa_enabled=True,
        )
        response = await self._request(client, json=user)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'otp_required': True}

    async def test_login_user_not_exit(self, client: AsyncClient) -> None:
        user = UserLoginFactory()
        response = await self._request(client, json=user)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'User with this email does not exist'}

    async def test_login_user_not_verified(self, client: AsyncClient) -> None:
        user = UserLoginFactory()
        await User.create(
            email=user['email'],
            hashed_password=make_hashed_password(user['password']),
        )
        response = await self._request(client, json=user)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Please verify your email address'}

    async def test_login_user_verify_password(self, client: AsyncClient) -> None:
        user = UserLoginFactory()
        await User.create(
            email=user['email'],
            hashed_password=make_hashed_password(user['password']),
            verified=True
        )
        user['password'] = 'strongPassword2'
        response = await self._request(client, json=user)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'detail': 'Incorrect Email or Password'}
