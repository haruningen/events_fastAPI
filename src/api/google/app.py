from authlib.integrations.base_client import OAuthError
from fastapi import APIRouter
from starlette.responses import HTMLResponse

from config import oauth
from fastapi import APIRouter, Request

router = APIRouter(tags=['google'])


@router.get('/login')
async def google_login(request: Request):
    redirect_uri = request.url_for('google_auth')
    print(redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get('/auth')
async def google_auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = token.get('userinfo')
    if user:
        user = dict(user)
    return user
