import pytest
from aiohttp import ClientSession
from pytest_mock.plugin import MockerFixture

from config import settings
from data import TicketmasterDataHandler
from data.tests.fixtures.mock_response import MockResponse
from models import DataSource


@pytest.mark.unit
class TestLoadTicketmasterData:

    @pytest.fixture(autouse=True)
    async def make_patch(self, mocker: MockerFixture) -> None:
        with open(settings.BASE_DIR / 'data/tests/fixtures/ticketmaster_response.json') as f:
            resp = MockResponse(f.read(), 200)
        mocker.patch('aiohttp.ClientSession.get', return_value=resp)

    async def test_load_events(self) -> None:
        ds = DataSource(
            name='predicthq',
            handler='data.TicketmasterDataHandler',
            api_url='http://0.0.0.0:8080/',
            config={'load_images': False},
        )
        handler = TicketmasterDataHandler(ds)
        res = list()
        async with ClientSession() as session:
            async for event in handler.get_events(session):
                res.append(event)
        assert len(res) == 10
