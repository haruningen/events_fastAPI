from typing import Optional

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from config import settings
from models import User
from utils.users import make_token, verify_password


class AdminAuth(AuthenticationBackend):

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form['username'], form['password']
        assert username and isinstance(username, str), 'username must be provided'
        assert password and isinstance(password, str), 'password must be provided'

        user: Optional[User] = await User.first(email=username)

        if not user:
            return False

        if not (user.verified and (user.is_moderator or user.is_superuser)):
            return False

        if not verify_password(password, user.hashed_password):
            return False

        token = make_token(
            settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            settings.JWT_SECRET_KEY,
            {'user_id': user.id}
        )
        request.session.update({'token': token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get('token')

        if token:
            return None
        return RedirectResponse(request.url_for('admin:login'), status_code=302)
