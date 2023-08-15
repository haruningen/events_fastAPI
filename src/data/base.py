from abc import ABC, abstractmethod
from typing import Optional
from pydantic import BaseModel
from aiohttp import ClientSession

from models import DataSource


class BaseDataHandler(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some events seed.
    """

    config_schema: type[BaseModel]

    def __init__(self, ds: DataSource) -> None:
        self.ds = ds
        self.config: BaseModel = self.config_schema(**self.ds.config)

    @abstractmethod
    async def to_event(self, data: dict) -> Optional[dict]:
        pass

    @abstractmethod
    async def get_events(self, session: ClientSession) -> Optional[list[dict]]:
        pass
