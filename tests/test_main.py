from fastapi.testclient import TestClient
from app.main import app
import time

client = TestClient(app)

def test_create_short_key():
    response = client.post("/shorten", json={"url": "https://example.com"})
    assert response.status_code == 200
    assert "short_key" in response.json()

def test_redirect_to_url():
    response = client.post("/shorten", json={"url": "https://example.com"})
    short_key = response.json()["short_key"]
    response = client.get(f"/{short_key}", follow_redirects=False)
    assert response.status_code == 301
    assert "location" in response.headers
    assert response.headers["location"] == "https://example.com"

def test_expired_url():
    response = client.post("/shorten", json={"url": "https://example.com", "expiration": 1})
    short_key = response.json()["short_key"]
    time.sleep(60)  # Wait for the URL to expire
    response = client.get(f"/{short_key}")
    assert response.status_code == 404

def test_url_stats():
    response = client.post("/shorten", json={"url": "https://example.com"})
    short_key = response.json()["short_key"]
    client.get(f"/{short_key}")
    time.sleep(1)
    response = client.get(f"/stats/{short_key}")
    assert response.status_code == 200
    assert response.json()["views"] == 1
    client.get(f"/{short_key}")
    time.sleep(1)
    response = client.get(f"/stats/{short_key}")
    assert response.status_code == 200
    assert response.json()["views"] == 2

    
