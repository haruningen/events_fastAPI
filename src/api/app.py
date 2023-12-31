from fastapi import APIRouter

from .auth import router as auth_router
from .events import router as events_router
from .google import router as google_router
from .users import router as users_router

__all__ = ('router',)

router = APIRouter()
router.include_router(users_router, prefix='/users')
router.include_router(auth_router, prefix='/auth')
router.include_router(google_router, prefix='/google')
router.include_router(events_router, prefix='/events')


@router.get('/live')
async def live() -> dict:
    return {'live': 'ok'}
