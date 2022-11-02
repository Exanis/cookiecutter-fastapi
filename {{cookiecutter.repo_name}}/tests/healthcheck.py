from fastapi.testclient import TestClient


def test_healthcheck_route(client: 'TestClient'):
    response = client.get('/api/healthcheck')
    assert response.status_code == 204
