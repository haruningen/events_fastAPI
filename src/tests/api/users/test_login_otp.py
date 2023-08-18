from typing import Any

from httpx import AsyncClient, Response
from starlette import status

from tests.mixins import BaseTestCase


class TestUsers(BaseTestCase):
    url_name = 'login_otp'

    async def _request(self, client: AsyncClient, **kwargs: Any) -> Response:
        email = kwargs.pop('email')
        otp_code = kwargs.pop('otp_code', None)
        return await client.post(
            self.url_path(),
            json={'email': email, 'otp_code': otp_code} if otp_code else {'email': email, 'otp_code': ''} | kwargs
        )

    async def test_tfa_login_success(self, client: AsyncClient) -> None:
        user = await self.auth_user_tfa()
        response = await self._request(client, email=user.email, otp_code=self.get_otp_code(user.tfa_secret))
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'access_token' in data and 'refresh_token' in data

    async def test_tfa_login_wrong_code(self, client: AsyncClient) -> None:
        user = await self.auth_user_tfa()
        response = await self._request(client, email=user.email, otp_code='11111')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorized'}

    async def test_tfa_login_no_code(self, client: AsyncClient) -> None:
        user = await self.auth_user_tfa()
        response = await self._request(client, email=user.email)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'detail': 'OTP code is required'}

    async def test_tfa_login_no_user(self, client: AsyncClient) -> None:
        response = await self._request(client, email='test@test.te', otp_code='11111')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorized'}
