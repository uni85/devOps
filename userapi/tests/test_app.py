from src.app import app   # src correspond au dossier où se trouve ton app.py

def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
