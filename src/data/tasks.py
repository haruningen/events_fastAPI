import asyncio
import importlib
from logging import getLogger

from data.context import DataContext
from models import DataSource
from worker import celery

logger = getLogger(__name__)


async def load_data() -> None:
    handlers: list[DataSource] = await DataSource.get_list()
    for handler in handlers:
        module_name, class_name = handler.handler.rsplit('.', 1)
        module = importlib.import_module(module_name)
        cls = getattr(module, class_name)
        await DataContext(cls(ds=handler)).load_events()


@celery.task(name='load_data_task')  # type: ignore
def load_data_task() -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(load_data())
