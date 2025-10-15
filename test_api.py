from flaskHttpServer import app, subscribers

def setup_function():
    subscribers.clear()

def test_add_and_list():
    c = app.test_client()
    r = c.post("/add-subscriber", json={"name": "Alice", "url": "http://x"})
    assert r.status_code == 201
    r = c.get("/list-subscribers")
    assert r.status_code == 200
    assert r.get_json()["subscribers"]["Alice"] == "http://x"

def test_publish_notifies_all():
    c = app.test_client()
    c.post("/add-subscriber", json={"name": "A", "url": "u1"})
    c.post("/add-subscriber", json={"name": "B", "url": "u2"})
    r = c.post("/publish", json={"subject": "S", "payload": {"k": 1}})
    j = r.get_json()
    assert r.status_code == 200
    assert j["subject"] == "S"
    assert len(j["notified"]) == 2

def test_delete():
    c = app.test_client()
    c.post("/add-subscriber", json={"name": "A", "url": "u"})
    r = c.delete("/delete-subscriber/A")
    assert r.status_code == 200
    r = c.get("/list-subscribers")
    assert "A" not in r.get_json()["subscribers"]
