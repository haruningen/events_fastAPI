from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.depends import PaginationDeps, get_authed_user, get_db

__all__ = ('router',)

from api.events.schemas import EventDetailScheme, EventsListSchema
from api.schemas import MessageSchema
from models import Event, User

router = APIRouter(tags=['events'])


@router.get(
    '',
    summary='Get list of events',
    response_model=EventsListSchema
)
async def get_events(pagination: PaginationDeps) -> dict[str, Any]:
    events_list: list[Event] = await Event.get_list(limit=pagination.limit, offset=pagination.offset)
    total_count: Optional[int] = await Event.get_count()
    return {'items': events_list, 'count': total_count}


@router.get(
    '/my',
    summary='Get user list of events',
    response_model=EventsListSchema
)
async def get_user_events(
        pagination: PaginationDeps,
        user: User = Depends(get_authed_user),
) -> dict[str, Any]:
    events_list: list[Event] = await Event.get_list(
        Event.users.any(id=user.id),
        limit=pagination.limit,
        offset=pagination.offset
    )
    total_count: Optional[int] = await Event.get_count()
    return {'items': events_list, 'count': total_count}


@router.get('/{event_id}', summary='Get event info by id', response_model=EventDetailScheme)
async def get_event(event_id: int, user: User = Depends(get_authed_user)) -> Event:
    event: Optional[Event] = await Event.get(event_id)  # type: ignore[func-returns-value]
    if not event:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Event with this ID does not exist'
        )
    event.want_go = any(eu for eu in event.users if user.id == eu.id)  # type: ignore[attr-defined]
    return event


@router.post('/attend/{event_id}', summary='Attend event to user', response_model=MessageSchema)
async def attend(
        event_id: int,
        user: User = Depends(get_authed_user),
        _db: AsyncSession = Depends(get_db)
) -> dict[str, str]:
    event: Optional[Event] = await Event.get(event_id)  # type: ignore[func-returns-value]
    if not event:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Event with this ID does not exist'
        )
    event_user = [eu for eu in event.users if user.id == eu.id]
    if any(event_user):
        await event.remove_user(event_user[0], _db)
    else:
        await event.add_user(user, _db)
    return {'message': 'ok'}
