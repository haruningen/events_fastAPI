from abc import abstractmethod, ABC
from typing import Optional, Any

from aiohttp import ClientSession

from models import Event


class BaseDataHandler(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some events seed.
    """

    @abstractmethod
    async def to_event(self, data: Any) -> Optional[Event]:
        pass

    @abstractmethod
    async def get_events(self, session: ClientSession) -> Optional[list[Event]]:
        pass
