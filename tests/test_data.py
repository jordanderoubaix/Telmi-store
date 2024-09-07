from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the API"}

def test_get_data():
    response = client.get("/store")
    assert response.status_code == 200
    assert response.json() == {"data": "This is some data"}