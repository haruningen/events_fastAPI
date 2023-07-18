from fastapi import APIRouter, Depends

from api.depends import get_authed_user

__all__ = ('router',)

from api.users.schemas import UserBaseSchema
from common.auth import oauth2_scheme
from models import User

router = APIRouter()


@router.get('/me', summary='Get current user info', response_model=UserBaseSchema)
async def get_user(user: User = Depends(get_authed_user)) -> User:
    return user
