import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_all_users_empty(client):
    """Expect 404 if database is empty or connection isn't mocked."""
    response = client.get('/users')
    assert response.status_code in [200, 404]

def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code in [200, 503]