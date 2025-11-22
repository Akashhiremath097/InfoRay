import json
from web_app.app import app

def test_api_articles():
    client = app.test_client()
    response = client.get("/api/articles")
    assert response.status_code == 200
    assert isinstance(response.json, list)
