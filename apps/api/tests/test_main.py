import sys
import os

# Set test API key before importing the app
os.environ["API_KEY"] = "test-api-key-for-tests"

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to IFI Course Catalog API"
    assert "endpoints" in data


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_get_courses():
    response = client.get("/courses/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_course_not_found():
    response = client.get("/courses/ZZ9999")
    assert response.status_code == 404


def test_invalid_course_id_format():
    response = client.get("/courses/invalid!")
    assert response.status_code == 422


def test_create_course_requires_api_key():
    response = client.post("/courses/", json={
        "id": "TE1234",
        "title": "Test Course",
        "credits": 10,
        "department": "Test",
        "level": "bachelor",
    })
    assert response.status_code == 403


def test_delete_course_requires_api_key():
    response = client.delete("/courses/IN1000")
    assert response.status_code == 403


def test_create_course_with_api_key():
    import random
    course_id = f"TE{random.randint(1000, 9999)}"
    response = client.post(
        "/courses/",
        json={
            "id": course_id,
            "title": "Test Course",
            "credits": 10,
            "department": "Test",
            "level": "bachelor",
        },
        headers={"X-API-Key": "test-api-key-for-tests"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == course_id
    assert data["title"] == "Test Course"
