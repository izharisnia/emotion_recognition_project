from app import app

def test_home_ok():
    c = app.test_client()
    r = c.get("/")
    assert r.status_code == 200

def test_analyze_requires_text():
    c = app.test_client()
    r = c.post("/analyze", json={"transcript": ""})
    assert r.status_code == 400
