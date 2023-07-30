from starlette.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main() -> None:
    response = client.get('/api/live')
    assert response.status_code == 200
    assert response.json() == {'live': 'ok'}