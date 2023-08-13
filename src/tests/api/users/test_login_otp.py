from typing import Any

from httpx import AsyncClient, Response
from pyotp import TOTP
from starlette import status

from models import User
from tests.fixtures.factories import UserLoginTFAFactory
from tests.mixins import BaseTestCase
from utils.users import make_hashed_password


class TestUsers(BaseTestCase):
    url_name = 'login_otp'

    async def _request(self, client: AsyncClient, **kwargs: Any) -> Response:
        return await client.post(self.url_path(), **kwargs)

    async def test_tfa_login_success(self, client: AsyncClient) -> None:
        user = UserLoginTFAFactory()
        await User.create(
            email=user['email'],
            hashed_password=make_hashed_password(user['password']),
            verified=True,
            tfa_enabled=True,
            tfa_secret=user['tfa_secret']
        )
        response = await self._request(client,
                                       json={'email': user['email'], 'otp_code': TOTP(user['tfa_secret']).now()})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'access_token' in data and 'refresh_token' in data

    async def test_tfa_login_wrong_code(self, client: AsyncClient) -> None:
        user = UserLoginTFAFactory()
        await User.create(
            email=user['email'],
            hashed_password=make_hashed_password(user['password']),
            verified=True,
            tfa_enabled=True,
            tfa_secret=user['tfa_secret']
        )
        response = await self._request(client, json={'email': user['email'], 'otp_code': '11111'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorized'}

    async def test_tfa_login_no_code(self, client: AsyncClient) -> None:
        user = UserLoginTFAFactory()
        await User.create(
            email=user['email'],
            hashed_password=make_hashed_password(user['password']),
            verified=True,
            tfa_enabled=True,
            tfa_secret=user['tfa_secret']
        )
        response = await self._request(client, json={'email': user['email'], 'otp_code': ''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'detail': 'OTP code is required'}

    async def test_tfa_login_no_user(self, client: AsyncClient) -> None:
        user = UserLoginTFAFactory()
        response = await self._request(client, json={'email': user['email'], 'otp_code': '11111'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorized'}
