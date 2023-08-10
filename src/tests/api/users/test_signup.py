from typing import Any

from httpx import AsyncClient, Response
from starlette import status

from models import User
from tests.fixtures.factories import UserPasswordNotMatchFactory, UserSignUpFactory
from tests.mixins import BaseTestCase
from utils.users import make_hashed_password


class TestUsersSignUp(BaseTestCase):
    url_name = 'create_user'

    async def _request(self, client: AsyncClient, **kwargs: Any) -> Response:
        return await client.post(self.url_path(), **kwargs)

    async def test_create_user_success(self, client: AsyncClient) -> None:
        user = UserSignUpFactory()
        response = await self._request(client, json=user)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['email'] == user['email']
        assert data['avatar_url'] is None

    async def test_create_user_exist(self, client: AsyncClient) -> None:
        user = UserSignUpFactory()
        await User.create(
            email=user['email'],
            hashed_password=make_hashed_password(user['password'])
        )
        response = await self._request(client, json=user)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'detail': 'User with this email already exist'}

    async def test_create_user_passwords_dont_match(self, client: AsyncClient) -> None:
        user = UserPasswordNotMatchFactory()
        response = await self._request(client, json=user)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json()['detail'][0]['msg'] == 'Value error, Passwords do not match'
