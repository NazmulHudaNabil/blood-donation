from tests.helpers import register_payload


def _register_and_login(client, **overrides):
    client.post("/auth/register", json=register_payload(**overrides))
    login = client.post(
        "/auth/login",
        data={"username": overrides.get("email", "donor@example.com"), "password": overrides.get("password", "secret123")},
    )
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_get_me_requires_auth(client):
    res = client.get("/users/me")
    assert res.status_code == 401


def test_get_me_with_invalid_token(client):
    res = client.get("/users/me", headers={"Authorization": "Bearer not-a-real-token"})
    assert res.status_code == 401


def test_get_me_returns_profile(client):
    headers = _register_and_login(client)
    res = client.get("/users/me", headers=headers)
    assert res.status_code == 200
    assert res.json()["email"] == "donor@example.com"


def test_update_me(client):
    headers = _register_and_login(client)
    res = client.put(
        "/users/me",
        headers=headers,
        json={
            "name": "Updated Name",
            "phone": "01700000009",
            "blood_group_id": 3,
            "division_id": 3,
            "district_id": 1,
            "upazila_id": 149,
            "area": "Savar Bazar",
            "is_available": False,
        },
    )
    assert res.status_code == 200, res.text
    body = res.json()
    assert body["name"] == "Updated Name"
    assert body["blood_group_id"] == 3
    assert body["area"] == "Savar Bazar"
    assert body["is_available"] is False
