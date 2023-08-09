from typing import Optional

from aiohttp import ClientSession

from .base import BaseDataHandler
from models import Event


class DataContext:
    def __init__(self, handler: BaseDataHandler) -> None:
        self._handler = handler

    # Save events in DB
    async def load_events(self, session: ClientSession) -> None:
        result = await self._handler.get_events(session)
        for event in result:
            if not await Event.first(source=event.source, source_id=event.source_id):
                await Event.create(_obj=event)
