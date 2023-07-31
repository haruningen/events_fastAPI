from httpx import AsyncClient

from models import User
from tests.fixtures.factories import UserFactory, UserLoginFactory
from tests.mixins import BaseTestCase
from utils.users import make_hashed_password


class TestUsersLogin(BaseTestCase):
    url_name = 'login'

    async def test_login_user_success(self, httpx_client: AsyncClient) -> None:
        user = UserLoginFactory()
        await User.create(
            email=user['email'],
            hashed_password=make_hashed_password(user['password']),
            verified=True
        )
        response = await httpx_client.post(self.url_path(), json=user)
        assert response.status_code == 200
        data = response.json()
        assert 'access_token' in data and 'refresh_token' in data

    async def test_login_user_not_exit_fail(self, httpx_client: AsyncClient) -> None:
        user = UserLoginFactory()
        response = await httpx_client.post(self.url_path(), json=user)
        assert response.status_code == 401

    async def test_login_user_not_verified_fail(self, httpx_client: AsyncClient) -> None:
        user = UserLoginFactory()
        await User.create(
            email=user['email'],
            hashed_password=make_hashed_password(user['password']),
        )
        response = await httpx_client.post(self.url_path(), json=user)
        assert response.status_code == 401

    async def test_login_user_verify_password_fail(self, httpx_client: AsyncClient) -> None:
        user = UserLoginFactory()
        await User.create(
            email=user['email'],
            hashed_password=make_hashed_password(user['password']),
            verified=True
        )
        user['password'] = 'strongPassword2'
        response = await httpx_client.post(self.url_path(), json=user)
        assert response.status_code == 400