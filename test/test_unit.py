import pytest
from app import app

def test_invalid_user_id_type():
    """Ensure the app handles non-integer IDs correctly (Flask should return 404)."""
    with app.test_client() as client:
        response = client.get('/users/abc')
        assert response.status_code == 404

def test_add_user_missing_data():
    """Unit logic: check how the app behaves with missing JSON keys."""
    with app.test_client() as client:
        response = client.post('/users', json={'name': 'only-name'})
        assert response.status_code == 500 # Based on your current try/except block