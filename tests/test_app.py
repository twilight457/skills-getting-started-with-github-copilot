from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_presence():
    activity = "Chess Club"
    email = "alice.test@example.com"

    # Ensure clean state
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert f"Signed up {email}" in resp.json().get("message", "")

    get = client.get("/activities")
    assert email in get.json()[activity]["participants"]

    # cleanup
    client.post(f"/activities/{activity}/unregister?email={email}")
    assert email not in activities[activity]["participants"]


def test_unregister_nonexistent():
    activity = "Chess Club"
    email = "noone@example.com"

    # ensure not present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    resp = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code == 400


def test_unregister_success():
    activity = "Chess Club"
    email = "bob.test@example.com"

    # signup first if needed
    if email not in activities[activity]["participants"]:
        client.post(f"/activities/{activity}/signup?email={email}")

    resp = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]
