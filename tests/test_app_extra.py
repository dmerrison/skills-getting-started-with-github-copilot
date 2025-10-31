import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/", follow_redirects=False)
    # Should redirect to /static/index.html
    assert response.status_code in (307, 302)
    assert "/static/index.html" in response.headers.get("location", "")

def test_activity_participant_limits():
    # Fill up an activity to its max participants
    activity = "Maths Society"
    max_participants = 20
    # Clear all participants for a clean test state
    from src.app import activities
    activities[activity]["participants"] = []
    # Fill up
    for i in range(max_participants):
        email = f"testuser{i}@mergington.edu"
        response = client.post(f"/activities/{activity}/signup", params={"email": email})
        assert response.status_code == 200
    # Next signup should not be possible
    response = client.post(f"/activities/{activity}/signup", params={"email": "overflow@mergington.edu"})
    assert response.status_code == 400
    assert "Activity is full" in response.json()["detail"]

def test_get_activities_structure():
    response = client.get("/activities")
    data = response.json()
    for name, details in data.items():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details
        assert isinstance(details["participants"], list)

def test_signup_and_unregister_case_insensitive():
    activity = "Chess Club"
    email = "CaseTest@mergington.edu"
    # Remove if present
    client.post(f"/activities/{activity}/unregister", params={"email": email})
    # Sign up
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    # Unregister
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 200
