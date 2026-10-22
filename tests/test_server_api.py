"""
Tests for FastAPI Server & Endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from server import app


@pytest.fixture
def client():
    return TestClient(app)


def test_serve_index_html(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "CineMatch" in response.text
    assert "<!DOCTYPE html>" in response.text


def test_api_movies_search(client):
    response = client.get("/api/movies?q=dark&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "movies" in data
    assert len(data["movies"]) <= 5
    assert any("dark" in m["title"].lower() for m in data["movies"])


def test_api_movie_details_success(client):
    response = client.get("/api/movie/The%20Dark%20Knight")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "The Dark Knight"
    assert data["movie_id"] == 155
    assert "poster_url" in data
    assert "genres" in data
    assert "director" in data


def test_api_movie_details_not_found(client):
    response = client.get("/api/movie/NonexistentMovie123456789")
    assert response.status_code == 404


def test_api_recommend_success(client):
    response = client.get("/api/recommend/The%20Dark%20Knight?top_k=5")
    assert response.status_code == 200
    data = response.json()
    assert "query_movie" in data
    assert "recommendations" in data
    assert len(data["recommendations"]) == 5

    titles = [r["title"] for r in data["recommendations"]]
    assert "The Dark Knight" not in titles
    assert any("Batman" in t or "Dark Knight" in t for t in titles)

    for r in data["recommendations"]:
        assert "poster_url" in r
        assert "similarity_percentage" in r
        assert 0.0 <= r["similarity_score"] <= 1.0


def test_api_stats(client):
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["catalog_size"] == 4800
    assert data["vocabulary_size"] == 5000


def test_api_poster_endpoint(client):
    response = client.get("/api/poster/155")
    assert response.status_code == 200
    assert "image/jpeg" in response.headers.get("content-type", "")
    assert len(response.content) > 1000
