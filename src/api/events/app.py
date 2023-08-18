from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.depends import GetAuthUser, PaginationDeps, get_db
from api.events.schemas import EventDetailScheme, EventsListSchema
from api.schemas import MessageSchema
from models import Event, User

__all__ = ('router',)

router = APIRouter(tags=['events'])


@router.get(
    '',
    summary='Get list of events',
    response_model=EventsListSchema
)
async def get_events(pagination: PaginationDeps) -> dict[str, Any]:
    events_list: list[Event] = await Event.get_list(limit=pagination.limit, offset=pagination.offset)
    total_count: int = await Event.get_count()
    return {'items': events_list, 'count': total_count}


@router.get(
    '/my',
    summary='Get user list of events',
    response_model=EventsListSchema
)
async def get_user_events(
        pagination: PaginationDeps,
        user: User = Depends(GetAuthUser()),
) -> dict[str, Any]:
    events_list: list[Event] = await Event.get_list(
        Event.users.any(id=user.id),
        limit=pagination.limit,
        offset=pagination.offset
    )
    total_count: int = await Event.get_count()
    return {'items': events_list, 'count': total_count}


@router.get('/{event_id}', summary='Get event info by id', response_model=EventDetailScheme)
async def get_event(event_id: int, user: User = Depends(GetAuthUser(required=False))) -> Event:
    event: Optional[Event] = await Event.get(event_id)  # type: ignore[func-returns-value]
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Event with ID {event_id} does not exist'
        )
    if user:
        event.want_go = any(eu for eu in event.users if user.id == eu.id)  # type: ignore[attr-defined]
    return event


@router.post('/attend/{event_id}', summary='Attach event to user', response_model=MessageSchema)
async def attend_event(
        event_id: int,
        user: User = Depends(GetAuthUser()),
        _db: AsyncSession = Depends(get_db)
) -> dict[str, str]:
    event: Optional[Event] = await Event.get(event_id)  # type: ignore[func-returns-value]
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Event with ID {event_id} does not exist'
        )
    if event_user := next((eu for eu in event.users if user.id == eu.id), None):
        await event.remove_user(event_user, _db)
        message = 'The user has been removed from the event'
    else:
        await event.add_user(user, _db)
        message = 'The user has been added to the event'
    return {'message': message}
