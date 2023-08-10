from logging import getLogger

from aiohttp import ClientSession
from sqlalchemy.exc import IntegrityError

from config import settings
from models import Event
from utils.images import remove_image

from .base import BaseDataHandler

logger = getLogger(__name__)


class DataContext:
    def __init__(self, handler: BaseDataHandler) -> None:
        self._handler = handler

    # Save events in DB
    async def load_events(self) -> None:
        async with ClientSession() as session:
            async for event in self._handler.get_events(session):  # type: ignore[attr-defined]
                try:
                    await Event.create(**event)
                except IntegrityError:
                    # Log parse result and finish
                    logger.info(f'Events parsing finished for {self._handler.ds.name}')
                    if event.image_path:
                        await remove_image(f'{settings.MEDIA_ROOT}/{event.image_path}')
                    break
