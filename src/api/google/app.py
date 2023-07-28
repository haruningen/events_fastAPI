import re
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

from authlib.integrations.base_client import OAuthError
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi_users.password import PasswordHelper
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from api.depends import get_db
from config import settings
from models import OAuthAccount, User
from utils.mail import google_success_oauth
from utils.users import get_user_by_email, get_user_oauth, make_auth_tokens, make_hashed_password

router = APIRouter(tags=['google'])

# Set up OAuth
config_data = {'GOOGLE_CLIENT_ID': settings.GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': settings.GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url=settings.GOOGLE_OAUTH_URL,
    client_kwargs={'scope': 'openid email profile'},
)


@router.get('/login')
async def google_login(request: Request) -> RedirectResponse:
    redirect_uri = request.url_for('google_auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get('/auth')
async def google_auth(request: Request, _db: AsyncSession = Depends(get_db)) -> dict:
    try:
        data = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=error.error)
    userinfo = data.get('userinfo')
    if not userinfo:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='The user is not found')
    oauth_account = {
        'oauth_name': 'google',
        'access_token': data.get('access_token'),
        'account_id': userinfo.sub,
        'account_email': userinfo.email,
        'expires_at': data.get('expires_at'),
    }
    # Check if the oauth account exist
    if user_oauth := await get_user_oauth('google', userinfo.sub):
        # Update the oauth account
        user_id = user_oauth.user_id
        await user_oauth.update(oauth_account)
    else:
        # Check if the user exist
        if db_user := await get_user_by_email(userinfo.email):
            # Add the oauth account
            account = OAuthAccount(**oauth_account, user_id=db_user.id)
            _db.add(account)
            await _db.commit()
            await _db.refresh(account)
            user_id = db_user.id
        else:
            # Create the user and oauth account
            password_helper = PasswordHelper()
            password = password_helper.generate()
            user = User(
                email=userinfo.email,
                hashed_password=make_hashed_password(password),
                verified=True
            )
            _db.add(user)
            await _db.commit()
            await _db.refresh(user)
            if userinfo.picture:
                try:
                    await user.set_avatar_path_by_url(image=re.sub(r's\d+', 's0', userinfo.picture))
                finally:
                    await user.save(['avatar_path'])
            account = OAuthAccount(**oauth_account, user_id=user.id)
            _db.add(account)
            await _db.commit()
            await _db.refresh(account)
            google_success_oauth(userinfo.email, password)
            user_id = user.id
    return make_auth_tokens(str(user_id))
