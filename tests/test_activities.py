"""
Test activities API endpoints using AAA (Arrange-Act-Assert) pattern.
"""
def test_get_activities(client):
    # Arrange
    # (client fixture provides app state)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Confirm participant added
    get_resp = client.get("/activities")
    assert email in get_resp.json()[activity]["participants"]

def test_signup_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = "daniel@mergington.edu"  # Already signed up

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_unregister_success(client):
    # Arrange
    activity = "Chess Club"
    email = "daniel@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")

    # Assert
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]
    # Confirm participant removed
    get_resp = client.get("/activities")
    assert email not in get_resp.json()[activity]["participants"]

def test_unregister_not_signed_up(client):
    # Arrange
    activity = "Chess Club"
    email = "notregistered@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")

    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]
