from tests.helpers import register_payload


def test_donors_requires_blood_group_and_district(client):
    res = client.get("/donors")
    assert res.status_code == 422


def test_donors_search_returns_matching_available_donor(client):
    client.post("/auth/register", json=register_payload())
    res = client.get("/donors", params={"blood_group_id": 7, "district_id": 1})
    assert res.status_code == 200
    donors = res.json()
    assert len(donors) == 1
    assert donors[0]["name"] == "Test Donor"
    assert "email" not in donors[0]


def test_donors_search_filters_out_other_blood_groups(client):
    client.post("/auth/register", json=register_payload())
    res = client.get("/donors", params={"blood_group_id": 1, "district_id": 1})
    assert res.status_code == 200
    assert res.json() == []


def test_donors_search_respects_upazila_filter(client):
    client.post("/auth/register", json=register_payload())
    # A different upazila within the same district should not match.
    res = client.get("/donors", params={"blood_group_id": 7, "district_id": 1, "upazila_id": 145})
    assert res.status_code == 200
    assert res.json() == []


def test_donor_profile_not_found(client):
    res = client.get("/donors/999")
    assert res.status_code == 404


def test_donor_availability_toggle_requires_auth(client):
    res = client.patch("/donors/me/availability", json={"is_available": False})
    assert res.status_code == 401


def test_donor_availability_toggle_and_mark_donated(client):
    client.post("/auth/register", json=register_payload())
    login = client.post("/auth/login", data={"username": "donor@example.com", "password": "secret123"})
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    res = client.patch("/donors/me/availability", headers=headers, json={"is_available": False})
    assert res.status_code == 200
    assert res.json()["is_available"] is False
    assert "email" not in res.json()

    res = client.patch("/donors/me/donated", headers=headers)
    assert res.status_code == 200
    body = res.json()
    assert body["is_available"] is False
    assert body["last_donation_date"] is not None
