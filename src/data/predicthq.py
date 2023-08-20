from datetime import datetime

from aiohttp import ClientSession

from config import settings
from data.base import BaseDataHandler
from data.schemas import ParsedEventPredictHQSchema, PredictHQConfigSchema
from gen_typing import YieldAsync


class PredictHQDataHandler(BaseDataHandler):
    """
        The Strategy for get events from PredictHQ
    """

    config: PredictHQConfigSchema
    config_schema = PredictHQConfigSchema

    async def to_event(self, data: dict) -> dict:
        schema = ParsedEventPredictHQSchema(**data)
        return schema.model_dump()

    async def get_events(self, session: ClientSession) -> YieldAsync[dict]:
        page = 0
        headers = {
            'Authorization': f'Bearer {self.ds.secret}'
        }
        params = {
            'active.gt': datetime.today().strftime('%Y-%m-%d'),
            'offset': page * self.config.limit
        }
        next_page = True

        while settings.DATA_HANDLER_TOTAL_PAGE > page and next_page:
            page += 1
            params['offset'] = page * self.config.limit
            params['limit'] = self.config.limit
            res, next_page = await self.fetch_events(session, headers, params)

            for event in res:
                yield event

    async def fetch_events(self, session: ClientSession, headers: dict, params: dict) -> tuple[list[dict], bool]:
        events = list()
        async with session.get(self.ds.api_url, headers=headers, params=params) as response:
            fetch_data = await response.json()
            next_page = bool(fetch_data['next'])

            for event in fetch_data['results']:
                events.append(await self.to_event(event))

        return events, next_page
