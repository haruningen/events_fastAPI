from httpx import AsyncClient
from starlette import status

from models import User
from tests.fixtures.factories import UserLoginFactory
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
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'access_token' in data and 'refresh_token' in data

    async def test_login_user_not_exit(self, httpx_client: AsyncClient) -> None:
        user = UserLoginFactory()
        response = await httpx_client.post(self.url_path(), json=user)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'User with this email does not exist'}

    async def test_login_user_not_verified(self, httpx_client: AsyncClient) -> None:
        user = UserLoginFactory()
        await User.create(
            email=user['email'],
            hashed_password=make_hashed_password(user['password']),
        )
        response = await httpx_client.post(self.url_path(), json=user)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Please verify your email address'}

    async def test_login_user_verify_password(self, httpx_client: AsyncClient) -> None:
        user = UserLoginFactory()
        await User.create(
            email=user['email'],
            hashed_password=make_hashed_password(user['password']),
            verified=True
        )
        user['password'] = 'strongPassword2'
        response = await httpx_client.post(self.url_path(), json=user)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'detail': 'Incorrect Email or Password'}
