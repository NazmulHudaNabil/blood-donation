import datetime

from tests.helpers import VALID_LOCATION


def request_payload(**overrides):
    payload = {
        "requester_name": "Requester",
        "requester_phone": "01811000001",
        "patient_name": "Patient",
        "hospital": "DMCH",
        "units_needed": 2,
        "needed_by": (datetime.date.today() + datetime.timedelta(days=3)).isoformat(),
        **VALID_LOCATION,
    }
    payload.update(overrides)
    return payload


def test_create_request(client):
    res = client.post("/requests", json=request_payload())
    assert res.status_code == 200, res.text
    body = res.json()
    assert body["status"] == "pending"
    assert body["units_needed"] == 2


def test_create_request_rejects_past_needed_by(client):
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    res = client.post("/requests", json=request_payload(needed_by=yesterday))
    assert res.status_code == 422


def test_create_request_rejects_too_many_units(client):
    res = client.post("/requests", json=request_payload(units_needed=999))
    assert res.status_code == 422


def test_create_request_hospital_is_optional(client):
    res = client.post("/requests", json=request_payload(hospital=None))
    assert res.status_code == 200
    assert res.json()["hospital"] is None


def test_list_requests_only_returns_pending(client):
    created = client.post("/requests", json=request_payload()).json()
    res = client.get("/requests")
    assert res.status_code == 200
    assert len(res.json()) == 1

    client.patch(f"/requests/{created['id']}/fulfill")
    res = client.get("/requests")
    assert res.json() == []


def test_list_requests_filters_by_blood_group_and_district(client):
    client.post("/requests", json=request_payload())
    res = client.get("/requests", params={"blood_group_id": 1, "district_id": 1})
    assert res.json() == []

    res = client.get("/requests", params={"blood_group_id": 7, "district_id": 1})
    assert len(res.json()) == 1


def test_fulfill_unknown_request_returns_404(client):
    res = client.patch("/requests/999/fulfill")
    assert res.status_code == 404
