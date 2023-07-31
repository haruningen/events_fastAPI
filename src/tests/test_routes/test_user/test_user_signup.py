from httpx import AsyncClient

from models import User
from tests.fixtures.factories import UserFactory, UserPasswordNotMatchFactory
from tests.mixins import BaseTestCase
from utils.users import make_hashed_password


class TestUsersSignUp(BaseTestCase):
    url_name = 'create_user'

    async def test_create_user_success(self, httpx_client: AsyncClient) -> None:
        user = UserFactory()
        response = await httpx_client.post(self.url_path(), json=user)
        assert response.status_code == 200
        data = response.json()
        assert data['email'] == user['email']
        assert data['avatar_url'] is None

    async def test_create_user_exist_fail(self, httpx_client: AsyncClient) -> None:
        user = UserFactory()
        await User.create(
            email=user['email'],
            hashed_password=make_hashed_password(user['password'])
        )
        response = await httpx_client.post(self.url_path(), json=user)
        assert response.status_code == 400


    async def test_create_user_passwords_dont_match_fail(self, httpx_client: AsyncClient) -> None:
        user = UserPasswordNotMatchFactory()
        response = await httpx_client.post(self.url_path(), json=user)
        assert response.status_code == 422