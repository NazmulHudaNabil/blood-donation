def test_list_blood_groups(client):
    res = client.get("/blood-groups")
    assert res.status_code == 200
    names = {b["name"] for b in res.json()}
    assert names == {"A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"}


def test_list_divisions(client):
    res = client.get("/locations/divisions")
    assert res.status_code == 200
    assert len(res.json()) == 8


def test_list_all_districts_flat(client):
    res = client.get("/locations/districts")
    assert res.status_code == 200
    assert len(res.json()) == 64


def test_list_districts_by_division(client):
    # division_id 3 is Dhaka.
    res = client.get("/locations/divisions/3/districts")
    assert res.status_code == 200
    names = {d["name"] for d in res.json()}
    assert "Dhaka" in names


def test_list_upazilas_by_district(client):
    # district_id 1 is Dhaka district.
    res = client.get("/locations/districts/1/upazilas")
    assert res.status_code == 200
    names = {u["name"] for u in res.json()}
    assert "Savar" in names
