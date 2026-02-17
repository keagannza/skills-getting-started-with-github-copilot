import pytest
from fastapi.testclient import TestClient

import copy
from src.app import app, activities

# Save the initial state of activities
initial_activities = copy.deepcopy(activities)

@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update(copy.deepcopy(initial_activities))

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    activity = "Chess Club"
    email = "pytestuser@mergington.edu"
    # Ensure not present
    client.delete(f"/activities/{activity}/unregister?email={email}")
    # Signup
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    # Unregister
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]
    # Unregister again should fail
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 404

def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=foo@bar.com")
    assert response.status_code == 404

def test_unregister_invalid_activity():
    response = client.delete("/activities/Nonexistent/unregister?email=foo@bar.com")
    assert response.status_code == 404
