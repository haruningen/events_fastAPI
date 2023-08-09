import asyncio
from logging import getLogger
import importlib
import aiohttp

from data import TicketmasterDataHandler
from data.context import DataContext
from models import DataSource
from worker import celery

logger = getLogger(__name__)


@celery.task(name="load_data")
async def load_data():
    handlers: list[DataSource] = await DataSource.get_list()
    tasks = list()
    async with aiohttp.ClientSession() as session:
        for handler in handlers:
            module_name, class_name = handler.handler.rsplit(".", 1)
            module = importlib.import_module(module_name)
            cls = getattr(module, class_name)
            await DataContext(cls()).load_events(session)
        result = await asyncio.gather(*tasks)
