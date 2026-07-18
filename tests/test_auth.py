from tests.helpers import register_payload


def test_register_success(client):
    res = client.post("/auth/register", json=register_payload())
    assert res.status_code == 200, res.text
    body = res.json()
    assert body["email"] == "donor@example.com"
    assert body["is_available"] is True
    assert "password" not in body


def test_register_duplicate_email_rejected(client):
    client.post("/auth/register", json=register_payload())
    res = client.post("/auth/register", json=register_payload(phone="01700000002"))
    assert res.status_code == 400
    assert "email" in res.json()["detail"].lower()


def test_register_duplicate_phone_rejected(client):
    client.post("/auth/register", json=register_payload())
    res = client.post("/auth/register", json=register_payload(email="someoneelse@example.com"))
    assert res.status_code == 400
    assert "phone" in res.json()["detail"].lower()


def test_register_rejects_unknown_blood_group(client):
    res = client.post("/auth/register", json=register_payload(blood_group_id=999))
    assert res.status_code == 422


def test_register_rejects_district_not_in_division(client):
    # district_id 1 is Dhaka district, which belongs to division_id 3 — not 1.
    res = client.post("/auth/register", json=register_payload(division_id=1))
    assert res.status_code == 422


def test_register_rejects_short_password(client):
    res = client.post("/auth/register", json=register_payload(password="ab1"))
    assert res.status_code == 422


def test_register_rejects_password_without_digit(client):
    res = client.post("/auth/register", json=register_payload(password="onlyletters"))
    assert res.status_code == 422


def test_login_success(client):
    client.post("/auth/register", json=register_payload())
    res = client.post("/auth/login", data={"username": "donor@example.com", "password": "secret123"})
    assert res.status_code == 200, res.text
    body = res.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_wrong_password(client):
    client.post("/auth/register", json=register_payload())
    res = client.post("/auth/login", data={"username": "donor@example.com", "password": "wrongpass"})
    assert res.status_code == 401


def test_login_unknown_email(client):
    res = client.post("/auth/login", data={"username": "nobody@example.com", "password": "secret123"})
    assert res.status_code == 401


def test_register_rate_limited_after_five_per_minute(client):
    for i in range(5):
        res = client.post("/auth/register", json=register_payload(email=f"user{i}@example.com", phone=f"0170000{i:04d}"))
        assert res.status_code == 200
    res = client.post("/auth/register", json=register_payload(email="oneMore@example.com", phone="01700009999"))
    assert res.status_code == 429
