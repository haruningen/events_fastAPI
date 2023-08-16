from typing import Any

from httpx import AsyncClient, Response
from starlette import status

from tests.mixins import BaseTestCase


class TestUsers(BaseTestCase):
    url_name = 'disable_tfa'

    async def _request(self, client: AsyncClient, **kwargs: Any) -> Response:
        token = kwargs.pop('token', None)
        otp_code = kwargs.pop('otp_code', None)
        headers = {'Authorization': f'Bearer {token}'} if token else {}
        return await client.post(
            self.url_path(),
            headers=headers,
            json={'otp_code': otp_code} | kwargs,
        )

    async def test_tfa_disable_success(self, client: AsyncClient) -> None:
        user = await self.auth_user_tfa()
        token = await self.authorized_user_token(user)
        response = await self._request(client, token=token, otp_code=self.get_otp_code(user.tfa_secret))
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'message': '2-Step Verification Removed Successfully'}

    async def test_tfa_disable_with_wrong_code(self, client: AsyncClient) -> None:
        user = await self.auth_user_tfa()
        token = await self.authorized_user_token(user)
        response = await self._request(client, token=token, otp_code='11111')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorized'}

    async def test_tfa_disable_no_code(self, client: AsyncClient) -> None:
        user = await self.auth_user_tfa()
        token = await self.authorized_user_token(user)
        response = await self._request(client, token=token, otp_code='')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'detail': 'OTP code is required'}

    async def test_user_unauthorized_without_token(self, client: AsyncClient) -> None:
        await self._test_user_unauthorized_without_token(client)

    async def test_unauthorized_with_fake_token(self, client: AsyncClient) -> None:
        await self._test_unauthorized_with_fake_token(client)
