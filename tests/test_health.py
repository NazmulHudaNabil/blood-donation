def test_health_ok(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok", "database": "ok"}


def test_home(client):
    res = client.get("/")
    assert res.status_code == 200
